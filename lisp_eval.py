import math
import operator

class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __repr__(self):
        if self.imag == 0:
            return f"{self.real}"
        return f"#c({self.real} {self.imag})"

    def __add__(self, other):
        if isinstance(other, ComplexNumber):
             return ComplexNumber(self.real + other.real, self.imag + other.imag)
        elif isinstance(other, (int, float)):
            return ComplexNumber(self.real + other, self.imag)
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'Complex' and '{type(other)}'")

    def __sub__(self, other):
        if isinstance(other, ComplexNumber):
             return ComplexNumber(self.real - other.real, self.imag - other.imag)
        elif isinstance(other, (int, float)):
            return ComplexNumber(self.real - other, self.imag)
        else:
            raise TypeError(f"Unsupported operand type(s) for -: 'Complex' and '{type(other)}'")

    def __mul__(self, other):
        if isinstance(other, ComplexNumber):
            real_part = self.real * other.real - self.imag * other.imag
            imag_part = self.real * other.imag + self.imag * other.real
            return ComplexNumber(real_part, imag_part)

        elif isinstance(other, (int, float)):
            return ComplexNumber(self.real * other, self.imag)
        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'Complex' and '{type(other)}'")

    def __truediv__(self, other):
        if isinstance(other, ComplexNumber):
            # Toto je AI (nevedel jsem jak funguje deleni complexnich cisel)
            denom = other.real ** 2 + other.imag ** 2  # c^2 + d^2
            real_part = (self.real * other.real + self.imag * other.imag) / denom
            imag_part = (self.imag * other.real - self.real * other.imag) / denom
            return ComplexNumber(real_part, imag_part)
        elif isinstance(other, (int, float)):
            return ComplexNumber(self.real / other, self.imag / other)
        else:
            raise TypeError(f"Unsupported operand type(s) for /: 'Complex' and '{type(other)}'")

    __radd__ = __add__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__
    __rsub__ = __sub__


class dotted_pair:

    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        if self.cdr == 'nil':
            return f"({self.car})"
        if isinstance(self.cdr, dotted_pair):
            return f"({self.car} {self.cdr.repr_cdr()}"

        return f"({self.car} . {self.cdr})"

    def __iter__(self):
        yield from lisp_to_list(self)

    def repr_cdr(self):
        if self.cdr == 'nil':
            return f"{self.car})"
        if isinstance(self.cdr, dotted_pair):
            return f"{self.car} {self.cdr.repr_cdr()}"

        return f"{self.car} . {self.cdr})"

def list_to_lisp(lst):
    if len(lst) == 0:
        return 'nil'
    rev = list(reversed(lst))
    elem = rev[0]

    if isinstance(elem, str):
        nothing, elem = parse_input(elem)

    if isinstance(elem, list):
        elem = list_to_lisp(elem)



    init_pair = dotted_pair(elem, 'nil')
    for element in rev[1:]:
        elem = element
        if isinstance(element, list):
            elem = list_to_lisp(element)
        if isinstance(element, str):
            nothing, elem = parse_input(element)
        init_pair = dotted_pair(elem,init_pair)
    return init_pair

def lisp_to_list(lisp):
    if lisp == 'nil':
        return []
    if isinstance(lisp.car, dotted_pair):
        return [lisp_to_list(lisp.car)] + lisp_to_list(lisp.cdr)
    return [lisp.car] + lisp_to_list(lisp.cdr)

class Enviroment:

    def __init__(self, parent, functions, symbols):
        self.parent = parent
        self.functions = functions
        self.symbols = symbols

    def find_symbol(self, symbol):
        if symbol in self.symbols:
            return self.symbols[symbol]
        if self.parent:
            return self.parent.find_symbol(symbol)
        raise Exception(f"Symbol {symbol} not found")

    def find_function(self, symbol):
        if symbol in self.functions:
            return self.functions[symbol]
        if self.parent:
            return self.parent.find_function(symbol)
        raise Exception(f"function {symbol} not found")

    def edit_symbol(self, symbol, value):
        self.symbols[symbol] = value
        return value

    def edit_function(self, symbol, value):
        self.functions[symbol] = value
        return symbol


class MacroList:

    def __init__(self,macros):
        self.macros = macros

    def edit_macro(self, symbol, value):
        self.macros[symbol] = value
        return symbol, value


class Function:

    def __init__(self, enviroment, args, body):
        self.enviroment = enviroment
        self.args = args
        self.body = body

    def __repr__(self):
        return f'<lambda-function {self.args}>'
    def __call__(self, *args):
        return eval_in_env(self.body, Enviroment(self.enviroment, dict(), (dict(zip(self.args, args)))))

def apply(func, args):
    return func(*args)

def created_list(*args):
    return list_to_lisp(list(args))

def parse_input(string):
    if '.' in string:
        return False, float(string)
    if string.replace('-', '').isnumeric():
        return False, int(string)
    return True, string


MACROS = MacroList({
})
GLOBAL_ENV = Enviroment(None,
                        {
                            '+': operator.add,
                            '-': operator.sub,
                            '*': operator.mul,
                            '/': operator.truediv,
                            'function': 'function',
                            'lambda': 'lambda',
                            'progn' : 'progn',
                            'funcall' : 'funcall',
                            'quote' : 'quote',
                            'if' : 'if',
                            'set!': 'set!',
                            'list': created_list,
                            'implicit-list': list,
                            'defun':'defun',
                            'defmacro':'defmacro',
                            'cons':(lambda x,y: dotted_pair(x,y)),
                            'car':(lambda x: x.car),
                            'cdr':(lambda x: x.cdr),
                            '=' : (lambda x,y: 't' if x == y else 'nil'),
                            '>' : (lambda x,y: 't' if x > y else 'nil'),
                            '<' : (lambda x,y: 't' if x < y else 'nil'),
                            'complex' : (lambda x,y: ComplexNumber(x,y)),
                            'realpart' : (lambda x: x.real),
                            'imagpart' : (lambda x: x.imag),
                            'apply' : apply,
                        },
                        {
                            'pi': math.pi,
                            'zero': 0,
                            'nil': 'nil',
                            't':'t',
                            'macros':MACROS.macros
                        })





def macro_compound_expand(op, args):
    if isinstance(op, list):
        return [op] + [macro_expand(expr) for expr in args]

    if op in MACROS.macros:
        return lisp_to_list(macro_expand(apply(MACROS.macros[op], args)))

    if op == 'quote':
        return [op] + args

    return [op] + [macro_expand(expr) for expr in args]

def macro_expand(expr):
    if isinstance(expr, list):
        if len(expr) >= 1:
            op = expr[0]
            return macro_compound_expand(op, expr[1:])
    return expr

def eval_in_env(expr, env):

    if isinstance(expr, list):
        op = expr[0]
        return compound_eval(op,expr[1:],env)

    if isinstance(expr, dotted_pair):
        return expr

    if isinstance(expr,(float,int)):
        return expr

    symbolp, symb = parse_input(expr)
    if symbolp:
        return env.find_symbol(symb)
    return symb

def compound_eval(op, args, env):
    op = env.find_function(op)
    match op:
        case 'lambda':
            return Function(env,tuple(args[0]), ['progn', *args[1:]])

        case 'progn':
            if len(args) == 0:
                return 'nil'
            return list(map(lambda x: (eval_in_env(x, env)), args))[-1]

        case 'funcall':
            if len(args) == 1:
                return handle_funcall(args[0],[], env)
            return handle_funcall(args[0],args[1:],env)

        case 'if':
            return handle_if(args[0], args[1:], env)

        case 'function':
            if len(args) == 1:
                return env.find_function(args[0])
            raise Exception("function takes only one argument")

        case 'quote':
            if len(args) == 1:
                if isinstance(args[0],list):
                    return list_to_lisp(args[0])
                return args[0]
            raise Exception("quote takes only one argument")

        case 'set!':
            if len(args) == 2:
                return env.edit_symbol(args[0], eval_in_env(args[1],env))
            raise Exception("set! takes two arguments")

        case 'defun':
            if len(args) == 2:
                return GLOBAL_ENV.edit_function(args[0], eval_in_env(args[1], env))
            raise Exception("defun takes two args name and lambda function")

        case 'defmacro':
            if len(args) == 2:
                return MACROS.edit_macro(args[0], eval_in_env(args[1], env))
            raise Exception("defmacro takes two args name and lambda function")

    return apply(op, (eval_in_env(expr, env) for expr in args))

def handle_funcall(op,args,env):
    op = eval_in_env(op, env)
    return apply(op, (eval_in_env(expr, env) for expr in args))

def handle_if(condition,args,env):
    if eval_in_env(condition,env) == 'nil':
        return eval_in_env(args[1],env)
    return eval_in_env(args[0], env)

def evaluate(expr):
    return eval_in_env((macro_expand(expr)),GLOBAL_ENV)

