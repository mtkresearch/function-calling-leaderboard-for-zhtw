# berkeley-function-call-leaderboard-for-zhtw 
# Introduction
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


