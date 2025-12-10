import jaconv

def preprocess(text: str) -> str:
    text = text.strip()
    text = jaconv.h2z(text, kana=True, ascii=True, digit=True)
    return text + "。" if not text.endswith(("。", "？", "！")) else text