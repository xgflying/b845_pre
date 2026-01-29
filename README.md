# flux and field calc
find electric flux and field by Gauss law

## 本地运行
## 创建虚拟环境并安装依赖
``` 
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```
## 启动测试用例
``` 
    python -m pytest -q
```
## 直接运行项目
``` 
    python -m field_calc.cli clear
    python -m field_calc.cli add 1e-6 0 0 0
    python -m field_calc.cli eval 0.05 0 0
```

## Usage
Legacy (single point charge at distance r):
    field-calc <charge_in_C> [radius_in_m|"r"]

Examples:
    $ field-calc 1e-6
    Electric flux: 1.129e+05 N·m²/C
    Electric field: 8.988e+03/(r**2) N/C

    $ field-calc 1e-6 0.1
    Electric flux: 1.129e+17 N·m²/C
    Electric field at r=0.1 m: 8.992e+09 N/C

Multiple point charges (Cartesian coordinates, persistent between shell commands):
    field-calc add <q_C> <x_m> <y_m> <z_m> [--label LABEL] [--state PATH]
    field-calc list [--state PATH]
    field-calc drop <id> [--state PATH]
    field-calc clear [--state PATH]
    field-calc field <x_m> <y_m> <z_m> [--state PATH]
    field-calc potential <x_m> <y_m> <z_m> [--state PATH]
    field-calc eval <x_m> <y_m> <z_m> [--state PATH]

By default, charges are stored in ~/.field_calc_charges.json. You can override with --state or by setting FIELD_CALC_STATE.

Example workflow:
    $ field-calc clear
    $ id1=$(field-calc add 1e-6 0 0 0 --label center)
    $ id2=$(field-calc add -1e-6 0.1 0 0 --label right)
    $ field-calc list
    $ field-calc eval 0.05 0 0
    $ field-calc drop "$id2"
    $ field-calc eval 0.05 0 0
