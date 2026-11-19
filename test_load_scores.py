import pytest
from load_scores import load_scores

def 만들기(tmp_path, 내용):
    파일 = tmp_path / "임시.csv"
    파일.write_text(내용, encoding="utf-8")
    return 파일

def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5

def test_빈_줄은_건너뛴다(tmp_path):
    파일 = 만들기(tmp_path, "name,score\n김하나,88\n\n이두리,92\n\n박세나,75\n")
    kept, skipped = load_scores(파일)
    assert len(kept) == 3

def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    파일 = 만들기(tmp_path, 'name,score\n"김, 하나",88\n')
    kept, skipped = load_scores(파일)
    assert len(kept) == 1

def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")

def test_헤더만_있으면_빈_결과(tmp_path):
    파일 = 만들기(tmp_path, "name,score\n")
    kept, skipped = load_scores(파일)
    assert kept == []
    assert skipped == []

@pytest.mark.parametrize("점수, 유효한가", [
    (-1, False),
    (0, True),
    (1, True),
    (99, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, 점수, 유효한가):
    파일 = 만들기(tmp_path, f"name,score\n홍길동,{점수}\n")
    kept, skipped = load_scores(파일)
    assert (len(kept) == 1) == 유효한가

def test_이름이_비어_있으면_건너뛴다(tmp_path):
    파일 = 만들기(tmp_path, "name,score\n,80\n")
    kept, skipped = load_scores(파일)
    assert len(kept) == 0
    assert len(skipped) == 1