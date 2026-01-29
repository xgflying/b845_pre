import sys

from .core import (
    add_charge,
    clear_charges,
    drop_charge,
    electric_field,
    electric_field_at_point,
    electric_field_magnitude,
    electric_flux,
    electric_potential_at_point,
    load_charges,
)


def _legacy_mode(argv):
    if len(argv) not in (2, 3):
        return False
    try:
        float(argv[1])
    except ValueError:
        return False
    return True


def _run_legacy(argv):
    q = float(argv[1])
    r_arg = argv[2] if len(argv) == 3 else "r"

    electric_flux(q)
    if r_arg == "r":
        electric_field(q, "r")
        return 0

    try:
        r = float(r_arg)
    except ValueError:
        print('Error: radius must be a number or "r"')
        return 1

    electric_field(q, r)
    return 0


def _usage():
    return "\n".join(
        [
            "Usage:",
            '  field-calc <charge_in_C> [radius_in_m|"r"]',
            "",
            "Multiple point charges (persistent state):",
            "  field-calc add <q_C> <x_m> <y_m> <z_m> [--label LABEL] [--state PATH]",
            "  field-calc list [--state PATH]",
            "  field-calc drop <id> [--state PATH]",
            "  field-calc clear [--state PATH]",
            "  field-calc field <x_m> <y_m> <z_m> [--state PATH]",
            "  field-calc potential <x_m> <y_m> <z_m> [--state PATH]",
            "  field-calc eval <x_m> <y_m> <z_m> [--state PATH]",
        ]
    )


def _extract_option(rest, name):
    if name not in rest:
        return None, rest
    idx = rest.index(name)
    if idx == len(rest) - 1:
        raise ValueError(f"Missing value for {name}")
    value = rest[idx + 1]
    new_rest = rest[:idx] + rest[idx + 2 :]
    return value, new_rest


def _format_charge(ch):
    label = ch.get("label")
    label_part = f' label="{label}"' if label is not None else ""
    return f'{ch["id"]}{label_part} q={ch["q"]}C pos=({ch["x"]},{ch["y"]},{ch["z"]})m'


def main(argv=None):
    argv = argv if argv is not None else sys.argv

    if _legacy_mode(argv):
        return _run_legacy(argv)

    if len(argv) < 2:
        print(_usage())
        return 1

    cmd = argv[1]
    rest = argv[2:]

    try:
        state, rest = _extract_option(rest, "--state")
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    if cmd == "add":
        try:
            label, rest = _extract_option(rest, "--label")
        except ValueError as e:
            print(f"Error: {e}")
            return 1

        if len(rest) != 4:
            print(_usage())
            return 1

        try:
            q = float(rest[0])
            x = float(rest[1])
            y = float(rest[2])
            z = float(rest[3])
        except ValueError:
            print("Error: q/x/y/z must be numbers")
            return 1

        charge_id = add_charge(q, x, y, z, label=label, state_path=state)
        print(charge_id)
        return 0

    if cmd == "list":
        charges = load_charges(state)
        if not charges:
            print("(no charges)")
            return 0
        for ch in charges:
            print(_format_charge(ch))
        return 0

    if cmd == "drop":
        if len(rest) != 1:
            print(_usage())
            return 1
        try:
            drop_charge(rest[0], state)
        except KeyError:
            print("Error: charge id not found")
            return 1
        return 0

    if cmd == "clear":
        if rest:
            print(_usage())
            return 1
        clear_charges(state)
        return 0

    if cmd not in ("field", "potential", "eval"):
        print(_usage())
        return 1

    if len(rest) != 3:
        print(_usage())
        return 1
    try:
        point = (float(rest[0]), float(rest[1]), float(rest[2]))
    except ValueError:
        print("Error: x/y/z must be numbers")
        return 1

    charges = load_charges(state)
    if not charges:
        print("Error: no charges in state. Use `field-calc add ...` first.")
        return 1

    if cmd == "field":
        e = electric_field_at_point(charges, point)
        mag = electric_field_magnitude(e)
        print(f"E=({e[0]:.6e},{e[1]:.6e},{e[2]:.6e}) N/C")
        print(f"|E|={mag:.6e} N/C")
        return 0

    if cmd == "potential":
        v = electric_potential_at_point(charges, point)
        print(f"V={v:.6e} V")
        return 0

    if cmd == "eval":
        e = electric_field_at_point(charges, point)
        mag = electric_field_magnitude(e)
        v = electric_potential_at_point(charges, point)
        print(f"E=({e[0]:.6e},{e[1]:.6e},{e[2]:.6e}) N/C")
        print(f"|E|={mag:.6e} N/C")
        print(f"V={v:.6e} V")
        return 0

    print(_usage())
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
