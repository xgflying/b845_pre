import math
import json
import os
import uuid

EPSILON_0 = 8.8541878128e-12
K_COULOMB = 1.0 / (4.0 * math.pi * EPSILON_0)

def electric_flux(q):
    flux = q / EPSILON_0  #point charge total flux
    print(f"Electric flux: {flux:.3e} N·m²/C")
    return flux

def electric_field(q, r='r'):
    if isinstance(r, str) and r == 'r':
        const = q / (4 * math.pi * EPSILON_0)
        print(f"Electric field: {const:.3e}/(r**2) N/C")
        return const
    else:
        E = q / (4 * math.pi * EPSILON_0 * r * r)  #find electric field at r
        print(f"Electric field at r={r} m: {E:.3e} N/C")
        return E

def electric_field_at_point(charges, point):
    px, py, pz = point
    ex = ey = ez = 0.0

    for ch in charges:
        q = float(ch["q"])
        dx = px - float(ch["x"])
        dy = py - float(ch["y"])
        dz = pz - float(ch["z"])
        r2 = dx * dx + dy * dy + dz * dz
        if r2 == 0.0:
            raise ValueError("Field is undefined at a charge location")
        r = math.sqrt(r2)
        inv_r3 = 1.0 / (r2 * r)
        scale = K_COULOMB * q * inv_r3
        ex += scale * dx
        ey += scale * dy
        ez += scale * dz

    return (ex, ey, ez)

def electric_potential_at_point(charges, point):
    px, py, pz = point
    v = 0.0

    for ch in charges:
        q = float(ch["q"])
        dx = px - float(ch["x"])
        dy = py - float(ch["y"])
        dz = pz - float(ch["z"])
        r2 = dx * dx + dy * dy + dz * dz
        if r2 == 0.0:
            raise ValueError("Potential is undefined at a charge location")
        r = math.sqrt(r2)
        v += K_COULOMB * q / r

    return v

def electric_field_magnitude(e_field):
    ex, ey, ez = e_field
    return math.sqrt(ex * ex + ey * ey + ez * ez)

def default_state_path():
    return os.environ.get("FIELD_CALC_STATE", os.path.expanduser("~/.field_calc_charges.json"))

def load_charges(state_path=None):
    path = state_path or default_state_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []

    if not isinstance(data, list):
        raise ValueError("Charge state file must contain a JSON list")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each charge must be a JSON object")
        for key in ("id", "q", "x", "y", "z"):
            if key not in item:
                raise ValueError("Each charge must include id, q, x, y, z")
    return data

def save_charges(charges, state_path=None):
    path = state_path or default_state_path()
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(charges, f, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp_path, path)

def add_charge(q, x, y, z, label=None, state_path=None):
    charges = load_charges(state_path)
    charge_id = uuid.uuid4().hex
    item = {
        "id": charge_id,
        "q": float(q),
        "x": float(x),
        "y": float(y),
        "z": float(z),
    }
    if label is not None:
        item["label"] = str(label)
    charges.append(item)
    save_charges(charges, state_path)
    return charge_id

def drop_charge(charge_id, state_path=None):
    charges = load_charges(state_path)
    kept = [c for c in charges if c.get("id") != charge_id]
    if len(kept) == len(charges):
        raise KeyError("Charge id not found")
    save_charges(kept, state_path)
    return len(charges) - len(kept)

def clear_charges(state_path=None):
    save_charges([], state_path)
