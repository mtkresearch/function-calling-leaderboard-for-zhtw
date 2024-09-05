from model_handler.model_style import ModelStyle

from model_handler.utils import (
    convert_to_tool,
    ast_parse,
    # convert_to_function_call,
    augment_prompt_by_languge,
    language_specific_pre_processing,
)
from model_handler.handler import BaseHandler
from vllm import LLM, SamplingParams
from mtkresearch.llm.chat import MRChatManager # TODO: move the mtkresearch folder 
from mtkresearch.llm.prompt import MRPromptV2 # TODO: move the mtkresearch folder 

import os, time, json
from collections import defaultdict


class BreezeHandler(BaseHandler):
    def __init__(self, model_name, temperature=0.7, top_p=1, max_tokens=1000) -> None:
        super().__init__(model_name, temperature, top_p, max_tokens)
        self.model_style = ModelStyle.Mistral
        self.params = SamplingParams(temperature=temperature, top_p=top_p, 
            max_tokens=max_tokens, stop_token_ids=[61876])
        self.pp = MRPromptV2(bos_token='<s>', eos_token='</s>')
        self.client = LLM(model="/path/to/model", tensor_parallel_size=2)

    def inference(self, prompt, functions, test_category):
        prompt = augment_prompt_by_languge(prompt, test_category)
        sys_prompt = "You are an helpful assistant who can access functions to help the user. Please always use the functions if possible, unless functions are not related to the user's questions. "
        if "FC" in self.model_name:
            functions = language_specific_pre_processing(functions, test_category)
            start = time.time()
            ma = MRChatManager(prompt=self.pp, sys_prompt=sys_prompt, functions=functions)
            ma.user_input(prompt)
            output_text = self._run(ma)
            latency = time.time() - start

            try:
                response = ma.parse_assistant(output_text)
                func_calls = response['func_calls']
                result = [
                    {func_call['name']: func_call['arguments']}
                    for func_call in func_calls
                ]
            except:
                result = [output_text]

        metadata = { # DBG: dummy metadata
            "input_tokens": [],
            "output_tokens": [],
            "latency": latency,
        }
        return result, metadata

    def decode_ast(self, result, language="Python"):
        if "FC" in self.model_name:
            decoded_output = []
            for invoked_function in result:
                name = list(invoked_function.keys())[0]
                params = json.dumps(invoked_function[name])
                params = json.loads(params)
                decoded_output.append({name: params})
            return decoded_output
        else:
            func = result
            func = func.replace("\\_", "_")
            if not func.startswith("["):
                func = "[" + func
            if not func.endswith("]"):
                func = func + "]"
            decoded_output = ast_parse(func, language)
            return decoded_output

    def decode_execute(self, result):
        if "FC" in self.model_name:
            function_call = self._convert_to_function_call(result)
            return function_call
        else:
            func = result
            func = func.replace("\\_", "_")
            decode_output = ast_parse(func)
            execution_list = []
            for function_call in decode_output:
                for key, value in function_call.items():
                    execution_list.append(
                        f"{key}({','.join([f'{k}={repr(v)}' for k, v in value.items()])})"
                    )
            return execution_list

    def _run(self, ma):
        output_text = self.client.generate(self.pp.get_prompt(ma.conversations, ma.functions).lstrip('<s>'), 
            self.params)[0].outputs[0].text

        return output_text
    
    def _convert_to_function_call(self, function_call_list):
        if type(function_call_list) == dict:
            function_call_list = [function_call_list]
        execution_list = []
        for function_call in function_call_list:
            for key, value in function_call.items():
                execution_list.append(
                    f"{key}({','.join([f'{k}={repr(v)}' for k,v in value.items()])})"
                )
        return execution_list
