import tiktoken
import pickle
import openai
import numpy as np
from pkg_resources import resource_filename

from config import openai_config
from utils.symbolic import train_trigram, get_words, vec_functions, scalar_functions
from utils.featurize import t_featurize_logprobs, score_ngram

class Ghostbuster(object):
    def __init__(self, tiktoken_encoder: str = "davinci-002", max_tokens: int = 2047) -> None:
        # Load tokenizer
        self.enc = tiktoken.encoding_for_model(tiktoken_encoder)

        # Load models
        model_path = resource_filename(__name__, "model/model")
        mu_path = resource_filename(__name__, "model/mu")
        sigma_path = resource_filename(__name__, "model/sigma")
        features_path = resource_filename(__name__, "model/features.txt")

        self.model = pickle.load(open(model_path, "rb"))
        self.mu = pickle.load(open(mu_path, "rb"))
        self.sigma = pickle.load(open(sigma_path, "rb"))
        self.best_features = open(features_path).read().strip().split("\n")
        self.trigram_model = train_trigram()

        self.MAX_TOKENS = max_tokens
        openai.api_key = openai_config["API_KEY"]


    def predict(self, text: str) -> float:
        # Load data and featurize
        tokens = self.enc.encode(text)[:self.MAX_TOKENS]
        doc = self.enc.decode(tokens).strip()

        print(f"Input: {doc}")

        # Train trigram
        print("Loading Trigram...")

        trigram = np.array(score_ngram(doc, self.trigram_model, self.enc.encode, n=3, strip_first=False))
        unigram = np.array(score_ngram(doc, self.trigram_model.base, self.enc.encode, n=1, strip_first=False))

        response = openai.Completion.create(
            model="babbage-002",
            prompt="<|endoftext|>" + doc,
            max_tokens=0,
            echo=True,
            logprobs=1,
        )
        ada = np.array(list(map(lambda x: np.exp(x), response["choices"][0]["logprobs"]["token_logprobs"][1:])))

        response = openai.Completion.create(
            model="davinci-002",
            prompt="<|endoftext|>" + doc,
            max_tokens=0,
            echo=True,
            logprobs=1,
        )
        davinci = np.array(list(map(lambda x: np.exp(x), response["choices"][0]["logprobs"]["token_logprobs"][1:])))

        subwords = response["choices"][0]["logprobs"]["tokens"][1:]
        gpt2_map = {"\n": "Ċ", "\t": "ĉ", " ": "Ġ"}
        for i in range(len(subwords)):
            for k, v in gpt2_map.items():
                subwords[i] = subwords[i].replace(k, v)

        t_features = t_featurize_logprobs(davinci, ada, subwords)

        vector_map = {
            "davinci-logprobs": davinci,
            "ada-logprobs": ada,
            "trigram-logprobs": trigram,
            "unigram-logprobs": unigram
        }

        exp_features = []
        for exp in self.best_features:

            exp_tokens = get_words(exp)
            curr = vector_map[exp_tokens[0]]

            for i in range(1, len(exp_tokens)):
                if exp_tokens[i] in vec_functions:
                    next_vec = vector_map[exp_tokens[i+1]]
                    curr = vec_functions[exp_tokens[i]](curr, next_vec)
                elif exp_tokens[i] in scalar_functions:
                    exp_features.append(scalar_functions[exp_tokens[i]](curr))
                    break

        data = (np.array(t_features + exp_features) - self.mu) / self.sigma
        prediction = self.model.predict_proba(data.reshape(-1, 1).T)[:, 1][0] # has form of [[HUMAN, AI]]

        return prediction