# berkeley-function-call-leaderboard-for-zhtw 
# Introduction
As the adoption of Large Language Models (LLMs) grows, evaluating their task-performing abilities—such as real-time information retrieval and external API call execution—becomes increasingly important. LLM performance varies significantly based on the language used, the number of functions called, and the specific user prompts. To address this variability, we propose a robust function-calling benchmark tailored to selected languages and diverse test data formats, ensuring consistent and reliable performance assessment across different use cases.

# Background
Research has highlighted a significant performance gap between high-resource languages, like English, and low-resource languages, such as Traditional Chinese, in multilingual models. English dominates the pre-training corpus, making up 89.7%, while Chinese(Traditional and Simplfied) constitutes only 0.13%. Even with fine-tuning, Chinese models perform worse than their English counterparts, particularly in the Traditional context, where only 20% is in Traditional Chinese. This results in inaccuracies and underscores the need for culturally and linguistically aligned datasets.

To address these issues in evaluating function-calling performance in Traditional Chinese, Gorilla's benchmarking method was chosen for its advantages. Gorilla offers automated API generation and invocation, supporting over 1,000 different APIs with a 95% accuracy rate. It enhances efficiency by saving development time and reducing error risks, making it a robust choice for improving the accuracy and relevance of language models in specific cultural contexts.










Berkeley Function Call Leaderboard for Traditional Chinese (zh-tw) is a fork of the [Berkeley Function Calling Leaderboard](https://github.com/original-repo-link), designed to support localized functionality for a Traditional Chinese function calling benchmark, specifically tailored for use in Taiwan. 
# New Features
<b>Language Configuration</b> and <b>Radar Chart Drawing</b> are the two features we have introduced to enhance the benchmarking process. These enhancements not only broaden the applicability of the benchmark but also improve the usability and depth of analysis for researchers and developers working with large language models.
## Language Configuration
This feature allows users to switch between languages via the command line, making the tool more accessible and flexible for multilingual users. By integrating datasets in various languages, users can compare the performance of large language models across different linguistic contexts, offering valuable insights for multilingual language model development.
These enhancements not only broaden the applicability of the benchmark but also improve the usability and depth of analysis for researchers and developers working with large language models.

## Radar Chart
Inspired by Berkeley Function-Calling Leaderboard's interactive wagon wheel tool, we have created a charting feature, aiming to help users create visualization of the benchmark outcomes and better understand the performance by the models. This visualization tool helps users easily understand and compare the performance of different models, providing a clear, graphical representation of their strengths and weaknesses. This chart is organized into nine categories: Irelevance Detection, Simple (AST), Multiple (AST), Parallel (AST), Parallel Multiple (AST), Simple (Exec), Multiple (Exec), Parallel (Exec), and Parallel Multiple (Exec).
### Install Dependencies
```bash
pip install -r requirements.txt # path可能還不確定看到時候requirements.txt要放root還是folder
```
### Usage
- Input: Each model should have exactly 9 scores enclosed in a list and in the following order: Irelevance Detection, Simple (AST), Multiple (AST), Parallel (AST), Parallel Multiple (AST), Simple (Exec), Multiple (Exec), Parallel (Exec), and Parallel Multiple (Exec).
- Recommendation: For readability, it is recommended to limit the number of models to 4, but more can be plotted if desired.
- Output: `radar_chart.png` will be created and saved in the current directory.

- Example usage
```bash
python chart.py "[10, 20, 30, 40, 50, 60, 70, 80, 90]" "[20, 30, 40, 50, 60, 70, 80, 90, 100]" "[30, 40, 50, 60, 70, 80, 90, 100, 110]"
```
![image](./radar_chart.png)

## Contributing and lisence


