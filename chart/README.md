# Berkeley Function Calling Leaderboard (BFCL)

💡 Read more in our [Gorilla OpenFunctions Leaderboard Blog](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)

🦍 Berkeley Function Calling Leaderboard live [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html#leaderboard)

🦍 Berkeley Function Calling Leaderboard on Hugginface [Berkeley Function Calling Leaderboard Huggingface](https://huggingface.co/spaces/gorilla-llm/berkeley-function-calling-leaderboard)

## Introduction
We introduce the Berkeley Function Leaderboard (BFCL), the **first comprehensive and executable function call evaluation dedicated to assessing Large Language Models' (LLMs) ability to invoke functions**. Unlike previous function call evaluations, BFCL accounts for various forms of function calls, diverse function calling scenarios, and their executability. Additionally, we release Gorilla-Openfunctions-v2, the most advanced open-source model to date capable of handling multiple languages, parallel function calls, and multiple function calls simultaneously. A unique debugging feature of this model is its ability to output an "Error Message" when the provided function does not suit your task.

Read more about the technical details and interesting insights in our [blog post](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)!

![image](./architecture_diagram.png)
### Install Dependencies

```bash
conda create -n BFCL python=3.10
conda activate BFCL
pip install -r requirements.txt # Inside gorilla/berkeley-function-call-leaderboard
pip install vllm==0.5.0 # If you have vLLM supported GPU(s) and want to run our evaluation data against self-hosted OSS models.
```


## Execution Evaluation Data Post-processing (Can be Skipped: Necesary for Executable Test Categories)
Add your keys into `function_credential_config.json`, so that the original placeholder values in questions, params, and answers will be reset.

To run the executable test categories, there are 4 API keys to include:

1. RAPID-API Key: https://rapidapi.com/hub

    * Yahoo Finance: https://rapidapi.com/sparior/api/yahoo-finance15
    * Real Time Amazon Data : https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-amazon-data
    * Urban Dictionary: https://rapidapi.com/community/api/urban-dictionary
    * Covid 19: https://rapidapi.com/api-sports/api/covid-193
    * Time zone by Location: https://rapidapi.com/BertoldVdb/api/timezone-by-location

    All the Rapid APIs we use have free tier usage. As a result, you need to subscribe to those API providers in order to have the executable test environment setup but it will be free of charge!

2. Exchange Rate API:https://www.exchangerate-api.com
3. OMDB API: http://www.omdbapi.com/apikey.aspx
4. Geocode API: https://geocode.maps.co/

The `apply_function_credential_config.py` will automatically search for dataset files in the default `./data/` directory and replace the placeholder values with the actual API keys.

```bash
python apply_function_credential_config.py
```


## Evaluating different models on the BFCL

Make sure the model API keys are included in your environment variables. Running proprietary models like GPTs, Claude, Mistral-X will require them.

```bash
export OPENAI_API_KEY=sk-XXXXXX
export MISTRAL_API_KEY=XXXXXX
export FIRE_WORKS_API_KEY=XXXXXX
export ANTHROPIC_API_KEY=XXXXXX
export COHERE_API_KEY=XXXXXX
export NVIDIA_API_KEY=nvapi-XXXXXX
export YI_API_KEY=XXXXXX
```

If decided to run OSS model, the generation script uses vllm and therefore requires GPU for hosting and inferencing. If you have questions or concerns about evaluating OSS models, please reach out to us in our [discord channel](https://discord.gg/grXXvj9Whz).

### Generating LLM Responses

Use the following command for LLM inference of the evaluation dataset with specific models

```bash
python openfunctions_evaluation.py --model MODEL_NAME --test-category TEST_CATEGORY
```

For available options for `MODEL_NAME` and `TEST_CATEGORY`, please refer to the [Models Available](#models-available) and [Available Test Category](#available-test-category) section below.

If no `MODEL_NAME` is provided, the model `gorilla-openfunctions-v2` will be used by default. If no `TEST_CATEGORY` is provided, all test categories will be run by default.


### Available Test Category
In the following two sections, the optional `--test-category` parameter can be used to specify the category of tests to run. You can specify multiple categories separated by spaces. Available options include:

- `all`: Run all test categories.
    - This is the default option if no test category is provided.
- `ast`: Abstract Syntax Tree tests.
- `executable`: Executable code evaluation tests.
- `python`: Tests specific to Python code.
- `non-python`: Tests for code in languages other than Python, such as Java and JavaScript.
- `python-ast`: Python Abstract Syntax Tree tests.
- Individual test categories:
    - `simple`: Simple function calls.
    - `parallel_function`: Multiple function calls in parallel.
    - `multiple_function`: Multiple function calls in sequence.
    - `parallel_multiple_function`: Multiple function calls in parallel and in sequence.
    - `executable_simple`: Executable function calls.
    - `executable_parallel_function`: Executable multiple function calls in parallel.
    - `executable_multiple_function`: Executable multiple function calls in sequence.
    - `executable_parallel_multiple_function`: Executable multiple function calls in parallel and in sequence.
    - `java`: Java function calls.
    - `javascript`: JavaScript function calls.
    - `rest`: REST API function calls.
    - `relevance`: Function calls with irrelevant function documentation.
- If no test category is provided, the script will run all available test categories. (same as `all`)

> If you want to run the `all` or `executable` or `python` category, make sure to register your REST API keys in `function_credential_config.json`. This is because Gorilla Openfunctions Leaderboard wants to test model's generated output on real world API!

> If you do not wish to provide API keys for REST API testing, set `test-category` to `ast` or any non-executable category.

> By setting the `--api-sanity-check` flag, or `-c` for short, if the test categories include `executable`, the evaluation process will perform the REST API sanity check first to ensure that all the API endpoints involved during the execution evaluation process are working properly. If any of them are not behaving as expected, we will flag those in the console and continue execution.


## Evaluating the LLM generations

### Running the Checker

Navigate to the `gorilla/berkeley-function-call-leaderboard/eval_checker` directory and run the `eval_runner.py` script with the desired parameters. The basic syntax is as follows:

```bash
python eval_runner.py --model MODEL_NAME --test-category {TEST_CATEGORY,all,ast,executable,python,non-python}
```

For available options for `MODEL_NAME` and `TEST_CATEGORY`, please refer to the [Models Available](#models-available) and [Available Test Category](#available-test-category) section.

If no `MODEL_NAME` is provided, all available model results will be evaluated by default. If no `TEST_CATEGORY` is provided, all test categories will be run by default.

### Example Usage

If you want to run all tests for the `gorilla-openfunctions-v2` model, you can use the following command:

```bash
python eval_runner.py --model gorilla-openfunctions-v2
```

If you want to evaluate all offline tests (do not require RapidAPI keys) for OpenAI GPT-3.5, you can use the following command:

```bash
python eval_runner.py --model gpt-3.5-turbo-0125 --test-category ast
```

If you want to run `rest` tests for a few Claude models, you can use the following command:

```bash
python eval_runner.py --model claude-3-5-sonnet-20240620 claude-3-opus-20240229 claude-3-sonnet-20240229 --test-category rest
```

If you want to run `rest` and `javascript` tests for a few models and `gorilla-openfunctions-v2`, you can use the following command:

```bash
python eval_runner.py --model gorilla-openfunctions-v2 claude-3-5-sonnet-20240620 gpt-4-0125-preview gemini-1.5-pro-preview-0514 --test-category rest javascript
```

### Model-Specific Optimization

Some companies have proposed some optimization strategies in their models' handler, which we (BFCL) think is unfair to other models, as those optimizations are not generalizable to all models. Therefore, we have disabled those optimizations during the evaluation process by default. You can enable those optimizations by setting the `USE_{COMPANY}_OPTIMIZATION` flag to `True` in the `model_handler/constants.py` file.