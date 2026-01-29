import pytest

from field_calc.core import (
    K_COULOMB,
    add_charge,
    clear_charges,
    drop_charge,
    electric_field_at_point,
    electric_field_magnitude,
    electric_potential_at_point,
    load_charges,
)


def test_single_charge_field_matches_coulomb_law():
    charges = [{"id": "c1", "q": 2e-6, "x": 0.0, "y": 0.0, "z": 0.0}]
    point = (0.25, 0.0, 0.0)
    e = electric_field_at_point(charges, point)
    mag = electric_field_magnitude(e)
    expected = K_COULOMB * charges[0]["q"] / (point[0] ** 2)
    assert e[0] == pytest.approx(expected, rel=1e-12)
    assert e[1] == pytest.approx(0.0, abs=0.0)
    assert e[2] == pytest.approx(0.0, abs=0.0)
    assert mag == pytest.approx(abs(expected), rel=1e-12)


def test_two_symmetric_charges_cancel_field_add_potential():
    q = 1e-6
    a = 0.2
    charges = [
        {"id": "l", "q": q, "x": -a, "y": 0.0, "z": 0.0},
        {"id": "r", "q": q, "x": a, "y": 0.0, "z": 0.0},
    ]
    point = (0.0, 0.0, 0.0)
    e = electric_field_at_point(charges, point)
    v = electric_potential_at_point(charges, point)
    assert e[0] == pytest.approx(0.0, abs=1e-12)
    assert e[1] == pytest.approx(0.0, abs=1e-12)
    assert e[2] == pytest.approx(0.0, abs=1e-12)
    assert v == pytest.approx(2.0 * K_COULOMB * q / a, rel=1e-12)


def test_undefined_at_charge_location_raises():
    charges = [{"id": "c1", "q": 1.0, "x": 1.0, "y": 2.0, "z": 3.0}]
    with pytest.raises(ValueError):
        electric_field_at_point(charges, (1.0, 2.0, 3.0))
    with pytest.raises(ValueError):
        electric_potential_at_point(charges, (1.0, 2.0, 3.0))


def test_state_add_list_drop_roundtrip(tmp_path):
    state = tmp_path / "charges.json"
    clear_charges(str(state))

    cid1 = add_charge(1e-6, 0, 0, 0, state_path=str(state))
    cid2 = add_charge(-2e-6, 1, 0, 0, label="neg", state_path=str(state))

    charges = load_charges(str(state))
    ids = {c["id"] for c in charges}
    assert {cid1, cid2} == ids

    removed = drop_charge(cid2, state_path=str(state))
    assert removed == 1

    charges2 = load_charges(str(state))
    ids2 = {c["id"] for c in charges2}
    assert ids2 == {cid1}
