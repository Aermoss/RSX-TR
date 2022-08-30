import pickle, hashlib, time, sys, os

from rsharp.main import keywords, constants, lexer, parser, interpreter
import rsharp.builder as builder
import rsharp.tools as tools

tools.read_file = lambda file: open(file, "r", encoding = "utf-8").read().replace("ana", "main")

keywords.update({
    "özdevimli": "AUTO",
    "geçversiz": "VOID",
    "boole": "BOOL",
    "tam": "INT",
    "kayan": "FLOAT",
    "dizgi": "STRING",
    "dön": "RETURN",
    "yanlış": "FALSE",
    "doğru": "TRUE",
    "boş": "NULL",
    "eğer": "IF",
    "yoksa": "ELSE",
    "iken": "WHILE",
    "için": "FOR",
    "eşleştir": "SWITCH",
    "dava": "CASE",
    "varsayılan": "DEFAULT",
    "sınıf": "CLASS",
    "görünür": "PUBLIC",
    "gizli": "PRIVATE",
    "korumalı": "PROTECTED",
    "dene": "TRY",
    "fırlat": "THROW",
    "yakala": "CATCH",
    "sabit": "CONST",
    "kullanarak": "USING",
    "yapı": "STRUCT",
    "yeni": "NEW",
    "sil": "DELETE",
    "yap": "DO",
    "adalanı": "NAMESPACE",
    "kes": "BREAK",
    "devam": "CONTINUE",
    "içer": "INCLUDE"
})

constants.update({
    "doğru": "BOOL",
    "yanlış": "BOOL"
})

def main():
    argv = sys.argv
    start_time = time.time()
    version = "tr-0.0.12"

    include_folders = ["./", f"{tools.get_dir()}/include/", f"{os.path.split(__file__)[0]}/include/"]
    if sys.platform == "win32": include_folders.append("C:\\RSharp\\include\\")
    console = True
    bytecode = True
    timeit = False
    get_tokens = False
    get_ast = False
    mode = None
    file = None

    for i in argv[1:]:
        if i[0] == "-":
            arg = i[1:].split("=")

            if arg[0][0] == "I":
                include_folders.insert(0, arg[0][1:])

            elif arg[0][:3] == "rmI":
                include_folders.pop(include_folders.index(arg[0][3:]))

            elif arg[0] == "timeit":
                if arg[1] == "true": timeit = True
                if arg[1] == "false": timeit = False

            elif arg[0] == "noconsole":
                if arg[1] == "true": console = False
                if arg[1] == "false": console = True

            elif arg[0] == "console":
                if arg[1] == "true": console = True
                if arg[1] == "false": console = False

            elif arg[0] == "gettok":
                if arg[1] == "true": get_tokens = True
                if arg[1] == "false": get_tokens = False

            elif arg[0] == "getast":
                if arg[1] == "true": get_ast = True
                if arg[1] == "false": get_ast = False

            elif arg[0] == "bytecode":
                if arg[1] == "true": bytecode = True
                if arg[1] == "false": bytecode = False

            else:
                tools.error(f"unknown operation '{i}'", file)

        elif i in ["version", "run", "build"]:
            if mode == None: mode = i
            else: tools.error("mode already setted", file)

        else:
            if file == None: file = i
            else: tools.error("file already setted", file)

    if mode == None: mode = "run"
    if file == None and mode != "version": tools.error("no input files", "rsharp", "fatal error", True)
    if file != None and mode != "version":
        if not os.path.isfile(file):
            tools.error("file not found", "rsharp", "fatal error", True)

    if mode == "run":
        if os.path.splitext(file)[1] not in [".rsx", ".rsxd", ".rsxc", ".rsxp", ".trx"]:
            tools.error(f"invalid extension: '{os.path.splitext(file)[1]}'", file)

        ast = None

        if os.path.splitext(file)[1] == ".rsxc":
            with open(os.path.splitext(file)[0] + ".rsxc", "rb") as f:
                content = pickle.loads(f.read())

                if "version" not in content:
                    tools.error("broken bytecode file", file)

                if content["version"] != version:
                    tools.error("bytecode version didn't match [bytecode: " + content["version"] + f", current: {version}]", file)

                ast = content["ast"]

        else:
            file_content = tools.read_file(file)

            if os.path.splitext(file)[0] + ".rsxc" in os.listdir() and bytecode:
                with open(os.path.splitext(file)[0] + ".rsxc", "rb") as f:
                    content = pickle.loads(f.read())

                    if "version" in content:
                        if content["version"] != version:
                            if content["file_content"] == hashlib.sha256(file_content.encode()).digest():
                                ast = content["ast"]

            if ast == None:
                tokens = lexer(file_content, file)
                if get_tokens: print(tokens)
                ast = parser(tokens, file)

                if bytecode:
                    content = {"ast": ast, "file_content": hashlib.sha256(file_content.encode()).digest(), "version": version}
                    with open(os.path.splitext(file)[0] + ".rsxc", "wb") as f: f.write(pickle.dumps(content))

        if get_ast: print(ast)
        interpreter(ast, file, True, False, {}, {}, None, {}, include_folders)

    elif mode == "build":
        if os.path.splitext(file)[1] not in [".rsx", ".rsxd", ".rsxc", ".rsxp"]:
            tools.error(f"invalid extension: '{os.path.splitext(file)[1]}'", file)

        variables, functions, library_functions, files, tokens, ast = tools.auto_include(
            file = file,
            include_folders = include_folders
        )

        if get_tokens: print(tokens)
        if get_ast: print(ast)

        builder.build_program(
            path = file,
            include_folders = include_folders,
            console = console,
            variables = variables,
            functions = functions,
            library_functions = library_functions,
            pre_included = files,
        )

    elif mode == "version":
        tools.set_text_attr(12)
        print(f"R# {version}", flush = True)
        tools.set_text_attr(7)

    else:
        tools.error("unknown error", file)

    if timeit:
        print("finished in:", time.time() - start_time)

    return 0

if __name__ == "__main__":
    sys.exit(main())