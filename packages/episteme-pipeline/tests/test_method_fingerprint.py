"""Tests for fine-grained LLM/embedding_model method fingerprinting."""

from episteme_pipeline.runs.fingerprints import fingerprint_method


class StubLLM:
    """Minimal stub mimicking an LLM runner object."""

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class StubEmbedModel:
    """Minimal stub mimicking an embedding_model runner object."""

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class StubLLMWithModel(StubLLM):
    """LLM stub with model_ref attribute."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


def test_fingerprint_method_null_returns_none() -> None:
    assert fingerprint_method(None) is None


def test_fingerprint_method_basic_class() -> None:
    llm = StubLLM(class_name="TestLLM")
    fp = fingerprint_method(llm)
    assert fp is not None
    assert isinstance(fp, str)


def test_fingerprint_method_captures_model_name() -> None:
    llm1 = StubLLM(class_name="TestLLM", model_name="gpt-4")
    llm2 = StubLLM(class_name="TestLLM", model_name="gpt-3.5")
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2


def test_fingerprint_method_captures_model_name_or_provider() -> None:
    llm1 = StubLLM(class_name="TestLLM", model_name_or_provider="claude-3-opus")
    llm2 = StubLLM(class_name="TestLLM", model_name_or_provider="claude-3-sonnet")
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2


def test_fingerprint_method_captures_model_ref() -> None:
    llm1 = StubLLMWithModel(class_name="TestLLM", model="meta/llama-3-70b")
    llm2 = StubLLMWithModel(class_name="TestLLM", model="google/gemma-2-27b")
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2


def test_fingerprint_method_captures_api_version() -> None:
    llm1 = StubLLM(class_name="TestLLM", api_version="2023-03-15")
    llm2 = StubLLM(class_name="TestLLM", api_version="2024-01-01")
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2


def test_fingerprint_method_captures_base_url() -> None:
    llm1 = StubLLM(class_name="TestLLM", base_url="https://openrouter.ai/api/v1")
    llm2 = StubLLM(class_name="TestLLM", base_url="https://api.openai.com/v1")
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2


def test_fingerprint_method_captures_temperature() -> None:
    llm1 = StubLLM(class_name="TestLLM", temperature=0.0)
    llm2 = StubLLM(class_name="TestLLM", temperature=0.7)
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2


def test_fingerprint_method_captures_max_tokens() -> None:
    llm1 = StubLLM(class_name="TestLLM", max_tokens=1024)
    llm2 = StubLLM(class_name="TestLLM", max_tokens=4096)
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2


def test_fingerprint_method_captures_top_p() -> None:
    llm1 = StubLLM(class_name="TestLLM", top_p=0.9)
    llm2 = StubLLM(class_name="TestLLM", top_p=1.0)
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2


def test_fingerprint_method_captures_n() -> None:
    llm1 = StubLLM(class_name="TestLLM", n=1)
    llm2 = StubLLM(class_name="TestLLM", n=3)
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2


def test_fingerprint_method_captures_embedding_dimensions() -> None:
    emb1 = StubEmbedModel(class_name="EmbedModel", dimensions=1536)
    emb2 = StubEmbedModel(class_name="EmbedModel", dimensions=768)
    fp1 = fingerprint_method(emb1)
    fp2 = fingerprint_method(emb2)
    assert fp1 != fp2


def test_fingerprint_method_captures_model_kwargs() -> None:
    llm1 = StubLLM(class_name="TestLLM", model_kwargs={"stop": ["\n\n"]})
    llm2 = StubLLM(class_name="TestLLM", model_kwargs={"stop": ["END."]})
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2


def test_fingerprint_method_deterministic() -> None:
    llm = StubLLM(
        class_name="TestLLM",
        model_name="gpt-4",
        temperature=0.5,
        max_tokens=2048,
        top_p=0.95,
        api_version="2024-01-01",
    )
    fp1 = fingerprint_method(llm)
    fp2 = fingerprint_method(llm)
    assert fp1 == fp2


def test_fingerprint_method_embedding_api_version() -> None:
    emb1 = StubEmbedModel(class_name="EmbedModel", embedding_api_version="v1")
    emb2 = StubEmbedModel(class_name="EmbedModel", embedding_api_version="v2")
    fp1 = fingerprint_method(emb1)
    fp2 = fingerprint_method(emb2)
    assert fp1 != fp2


def test_fingerprint_method_comprehensive_differs() -> None:
    llm1 = StubLLM(
        class_name="ChatLLM",
        model_name="gpt-4-turbo",
        model="gpt-4-turbo",
        api_version="2024-04-09",
        base_url="https://api.openai.com/v1",
        temperature=0.0,
        max_tokens=4096,
        top_p=0.1,
        n=1,
        model_kwargs={"logit_bias": {1234: 5.0}},
    )
    llm2 = StubLLM(
        class_name="ChatLLM",
        model_name="gpt-4-turbo",
        model="gpt-4-turbo",
        api_version="2024-04-09",
        base_url="https://api.openai.com/v1",
        temperature=0.1,
        max_tokens=4096,
        top_p=0.1,
        n=1,
        model_kwargs={"logit_bias": {1234: 5.0}},
    )
    fp1 = fingerprint_method(llm1)
    fp2 = fingerprint_method(llm2)
    assert fp1 != fp2
