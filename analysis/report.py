import argparse
import json


TEST_FILE_MAPPING = {
    "executable_simple": "gorilla_openfunctions_v1_test_executable_simple.json",
    "executable_parallel_function": "gorilla_openfunctions_v1_test_executable_parallel_function.json",
    "executable_multiple_function": "gorilla_openfunctions_v1_test_executable_multiple_function.json",
    "executable_parallel_multiple_function": "gorilla_openfunctions_v1_test_executable_parallel_multiple_function.json",
    "simple": "gorilla_openfunctions_v1_test_simple.json",
    "relevance": "gorilla_openfunctions_v1_test_relevance.json",
    "parallel_function": "gorilla_openfunctions_v1_test_parallel_function.json",
    "multiple_function": "gorilla_openfunctions_v1_test_multiple_function.json",
    "parallel_multiple_function": "gorilla_openfunctions_v1_test_parallel_multiple_function.json",
    # "rest": "gorilla_openfunctions_v1_test_rest.json",
}

def _get_problems(lang):
    problems = {}
    for key in TEST_FILE_MAPPING:
        instances = []
        for line in open(f'./data/{lang}/{TEST_FILE_MAPPING[key]}').readlines():
            instances.append(json.loads(line.strip()))
        problems[key] = instances
    return problems

def _get_results(lang, model_name):
    results = {}
    for key in TEST_FILE_MAPPING:
        instances = []
        path = f'./result/{lang}/{model_name}/{TEST_FILE_MAPPING[key]}'.replace('.json', '_result.json')
        try:
            for line in open(path).readlines():
                instances.append(json.loads(line.strip()))
            results[key] = instances
        except:
            continue
    return results

def _get_failures(lang, model_name):
    failures = {}
    for key in TEST_FILE_MAPPING:
        path = f'./score/{lang}/{model_name}/{key}_score.json'
        try:
            failed = {}
            for line in open(path).readlines()[1:]:
                data = json.loads(line.strip())
                failed[data['id']-1] = data

            failures[key] = failed
        except:
            continue
    return failures

def generate_report(model_name, lang, out_json):
    problems = _get_problems(lang)
    results = _get_results(lang, model_name)
    failures = _get_failures(lang, model_name)
    
    content = {}
    for key in problems:
        if key not in results:
            continue
        content[key] = []
        for i, (problem, result) in enumerate(zip(problems[key], results[key])):
            del result["id"]
            if "input_token_count" in result:
                del result["input_token_count"]
            if "output_token_count" in result:
                del result["output_token_count"]
            if "latency" in result:
                del result["latency"]

            if i in failures[key]:  # failed
                failed = failures[key][i]
                del failed["id"]
                del failed["model_name"]
                del failed["valid"]
                if "prompt" in failed:
                    del failed["prompt"]
                if "model_result_raw" in failed:
                    del failed["model_result_raw"]

                content[key].append(
                    {
                        'pass': False,
                        'problem': problem,
                        'failure': failed
                    }
                )
            else:
                continue
                # content[key].append(
                #     {
                #         'pass': True,
                #         'problem': problem,
                #         'result': result,
                #     }
                # )
    json.dump(content, open(out_json, 'w'), indent=2, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="gpt-3.5-turbo-0125-FC")
    parser.add_argument("--out_json", type=str, default='./score/zhtw/report_zhtw.json')
    parser.add_argument("--language", type=str, default="zhtw", help="Specify the language for the test cases and results")
    args = parser.parse_args()

    generate_report(args.model_name, args.language, args.out_json)