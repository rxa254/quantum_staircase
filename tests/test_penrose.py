from quantum_staircase.patterns import penrose

def test_penrose_generation():
    polys = penrose.generate_tiles(level=2)
    assert len(polys) > 0
