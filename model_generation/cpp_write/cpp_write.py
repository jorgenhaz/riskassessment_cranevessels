import sympy as sp
import numpy as np
import os

def vector_to_cppfn(m: sp.Matrix, name: str, indent: str = '\t', **kwargs):
    variables = set()
    for varlist in kwargs.values():

        if isinstance(varlist, list):
            variables.update(varlist)
        elif isinstance(varlist, sp.Symbol):
            variables.add(varlist)
        else:
            raise ValueError(f"Invalid type in kwargs: {varlist} (type: {type(varlist)})")
        
    assert m.free_symbols.issubset(
        variables), "All free symbols in the matrix must be in the variables list" + \
        f". {m.free_symbols} not in {variables}"

    identifier = "m"
    # Changing identifier if already exists
    while identifier in str(variables) or identifier == name:
        identifier += str(np.random.randint(0, 9))
    # Constructing the h-file
    declaration_h = f'#ifndef {name.upper()}_H\n'
    declaration_h += f'#define {name.upper()}_H\n\n'
    declaration_h += "#include <Eigen/Dense>\n\n"
    declaration_h += f"Eigen::VectorXd {name}("
    for i, (vname, vlist) in enumerate(kwargs.items()):
        if i > 0:
            declaration_h += ", "
        if isinstance(vlist, sp.Symbol):
            declaration_h += f"double {vlist}_in"
        else:
            declaration_h += f"Eigen::VectorXd {vname}"

    declaration_h += ");\n\n"
    declaration_h += "#endif"
    # Constructing the cpp-file
    declaration_cpp = f"Eigen::VectorXd {name}("
    for i, (vname, vlist) in enumerate(kwargs.items()):
        if i > 0:
            declaration_cpp += ", "
        if isinstance(vlist, sp.Symbol):
            declaration_cpp += f"double {vlist}_in"
        else:
            declaration_cpp += f"Eigen::VectorXd {vname}"

    declaration_cpp += ")"

    code = f'#include "{name}.h"\n\n'
    code += declaration_cpp + " {\n"
    for vname, vlist in kwargs.items():
        if isinstance(vlist, sp.Symbol):
            code += f"{indent}double {vlist} = {vname}_in;\n"
            continue
        for i, v in enumerate(vlist):
            code += f"{indent}double {v} = {vname}({i});\n"
    code += f"{indent}Eigen::VectorXd {identifier}({m.rows}, {m.cols});\n"
    rows, cols = m.shape
    for r in range(rows):
        expr = sp.ccode(m[r, 0])
        code += f"{indent}{identifier}({r}) = {expr};\n"
    code += f"{indent}return {identifier};\n" + "}"

    return code, declaration_h


def matrix_to_cppfn(m: sp.Matrix, name: str, indent: str = '\t', **kwargs):
    variables = {v for varlist in kwargs.values() for v in varlist}
    assert m.free_symbols.issubset(
        variables), "All free symbols in the matrix must be in the variables list"

    identifier = "m"
    # Change name of identifier if already exist
    while identifier in variables or identifier == name:
        identifier += str(np.random.randint(0, 9))
    # Constructing the h-file
    declaration_h = f'#ifndef {name.upper()}_H\n'
    declaration_h += f'#define {name.upper()}_H\n\n'
    declaration_h += "#include <Eigen/Dense>\n\n"
    declaration_h += f"Eigen::MatrixXd {name}("
    declaration_h += ", ".join(
        [f"Eigen::VectorXd {vname}" for vname in kwargs.keys()])
    declaration_h += ");\n\n"
    declaration_h += "#endif"
    # Constructing the cpp-file
    declaration_cpp = f"Eigen::MatrixXd {name}("
    declaration_cpp += ", ".join(
        [f"Eigen::VectorXd {vname}" for vname in kwargs.keys()])
    declaration_cpp += ")"

    # Generating the code
    code = f'#include "{name}.h"\n\n'
    code += declaration_cpp + " {\n"
    for vname, vlist in kwargs.items():
        for i, v in enumerate(vlist):
            code += f"{indent}double {v} = {vname}({i});\n"
    code += f"{indent}Eigen::MatrixXd {identifier}({m.rows}, {m.cols});\n"
    rows, cols = m.shape
    
    for r in range(rows):
        for c in range(cols):
            expr = sp.ccode(m[r, c])
            code += f"{indent}{identifier}({r}, {c}) = {expr};\n"
    code += f"{indent}return {identifier};\n" + "}"

    return code, declaration_h


def to_cppfn(m: sp.Matrix, name: str, indent: str = '\t', **kwargs):
    for key, value in kwargs.items():
        if isinstance(value, sp.Matrix):  # If value is sympy matrix
            kwargs[key] = list(value)  # Convert to list of symbols

    if m.shape[0] == 1 or m.shape[1] == 1:
        return vector_to_cppfn(m, name, indent, **kwargs)
    return matrix_to_cppfn(m, name, indent, **kwargs)

def generate_cpp_files(m, name, kwargs, output_dir_cpp="output", output_dir_h="output"):
    code, declaration = to_cppfn(m=m, name=name, kwargs=kwargs)

    os.makedirs(output_dir_cpp, exist_ok=True)
    with open(f"{output_dir_cpp}/{name}.cpp", "w") as cpp_file:
        cpp_file.write(code)

    os.makedirs(output_dir_h, exist_ok=True)
    with open(f"{output_dir_h}/{name}.h", "w") as h_file:
        h_file.write(declaration)