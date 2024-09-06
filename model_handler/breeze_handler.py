import json

from mtkresearch.llm.prompt import MRPromptV2 

from model_handler.oss_handler import OSSHandler


class BreezeHandler(OSSHandler):
    def __init__(self, model_name, temperature=0.01, top_p=0.01, max_tokens=1200) -> None:
        super().__init__(model_name, temperature, top_p, max_tokens)

        if model_name.endswith('rc3'):
            self.bos_token='<s>'
            self.eos_token='</s>'
            self.im_end_token_id = 61876
            self.prompt_template = MRPromptV2(bos_token=self.bos_token, eos_token=self.eos_token)
            self.model_path = '/kaggle/working/breeze-fc/'
        else:
            self.bos_token='<s>'
            self.eos_token='</s>'
            self.im_end_token_id = 61876
            self.prompt_template = MRPromptV2(bos_token=self.bos_token, eos_token=self.eos_token)
            self.model_path = '/kaggle/working/breeze-fc/'

    def _format_prompt(self, prompt, function, test_category):
        conversations = [
            {
                'role': 'user',
                'content': prompt
            }
        ]
        model_query = self.prompt_template.get_prompt(conversations, function).removeprefix(self.bos_token)
        return model_query

    def inference(
        self,
        test_question,
        num_gpus,
        gpu_memory_utilization,
    ):
        test_question = self.process_input(test_question, self._format_prompt)

        ans_jsons = self._batch_generate(
            test_question=test_question,
            model_path=self.model_path,
            temperature=0.01,
            max_tokens=1500,
            top_p=0.01,
            dtype=self.dtype,
            stop_token_ids=[self.im_end_token_id],
            num_gpus=num_gpus,
            gpu_memory_utilization=gpu_memory_utilization,
        )

        return ans_jsons, {"input_tokens": 0, "output_tokens": 0, "latency": 0}

    def decode_ast(self, result, language="Python"):
        conv = self.prompt_template.parse_generated_str(result)
        return [{x['function']['name']: json.loads(x['function']['arguments'])} 
                for x in conv['tool_calls']]

    def decode_execute(self, result):
        conv = self.prompt_template.parse_generated_str(result)
        return [{x['function']['name']: json.loads(x['function']['arguments'])} 
                for x in conv['tool_calls']]
