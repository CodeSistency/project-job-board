import pandas as pd
from app import data_processing as dp

def test_merge_comments():
    df = pd.DataFrame({
        'candidate_id': [1, 1, 2],
        'id': [100, 101, 200],
        'body': ['Comentario A', 'Comentario B', 'Comentario C'],
        'created_at': ['2024-01-01', '2024-01-02', '2024-01-03']
    })
    merged = dp.merge_comments(df)
    assert 1 in merged
    assert 2 in merged
    assert merged[1].count('\n\n') == 1
    assert '100 2024-01-01: Comentario A' in merged[1]
    assert '101 2024-01-02: Comentario B' in merged[1]
    assert merged[2] == '200 2024-01-03: Comentario C'

def test_clean_and_concat_names():
    row = pd.Series({'name': 'Juan', 'lastname': 'Pérez'})
    assert dp.clean_and_concat_names(row) == 'Juan Pérez'
    row2 = pd.Series({'name': 'Ana'})
    assert dp.clean_and_concat_names(row2) == 'Ana'
    row3 = pd.Series({'basic': 'Luis Gómez'})
    assert dp.clean_and_concat_names(row3) == 'Luis Gómez'
