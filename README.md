# Ghostbuster: Detecting Text <i>Ghostwritten</i> by Large Language Models

This is a fork of [Ghostbuster](https://github.com/vivek3141/ghostbuster) that has been modified to integrate more easily with other projects as a simple python package.

## Installation

To install the Ghostbuster package, run the following command:

```bash
pip install ghostbuster@git+https://github.com/vivek3141/ghostbuster.git
```

You may also need to open a `python` shell to install the following nltk `brown` model:

```python
import nltk
nltk.download('brown')
```

## Usage

To use the package, add your OpenAI key as an env variable called `OPENAI_API_KEY`, then create a file called `openai.config` in the main directory with the following template:

```json
openai_config = {
    "API_KEY": os.environ.get("OPENAI_API_KEY", None)
}
```

Now use the following code to detect ghostwritten text:

```python
from ghostbuster import Ghostbuster

ghostbuster = Ghostbuster()
ghostbuster.predict("I love you") # returns ~0.9967 after ~20s
```

## Disclaimer

Ghostbuster’s training data, which consists of news, student essay, and creative writing data, is not representative of all writing styles or topics and contains predominantly British and American English text. If you wish to apply Ghostbuster to real-world cases of potential off-limits usage of text generation, such as identifying ChatGPT-written student essays, be wary that incorrect predictions by Ghostbuster are particularly likely in the following cases:

<ul>
<li> For shorter text
<li> In domains that are further from those on which Ghostbuster was trained (e.g., text messages)
<li> For text in varieties of English besides American and British English, or in non-English languages
<li> For text written by non-native speakers of English
<li> For AI-generated text that has been edited or paraphrased by a human
</ul>

No AI-generated text detector is 100% accurate; we strongly discourage incorporation of Ghostbuster into any systems that automatically penalize students or other writers for alleged usage of text generation without human intervention. Privacy: Please be aware that all inputs to Ghostbuster are sent to the OpenAI API, and we also save the inputs for internal testing purposes. Though we will not distribute the data publicly, we cannot guarantee the privacy of any inputs to Ghostbuster.
