"""
Implementação do decorator conforme descrito no exercício 3
"""
def computed_property(*dependencies):
    """
    Decorator que cria uma proprietade computada com cache. 
    O valor só é recalculado se alguma dependência mudar.
    """
    def decorator(func):
        return ComputedProperty(func, dependencies)
    return decorator


class ComputedProperty:
    """
    Implementa um descriptor que calcula o valor de uma propriedade, 
    armazena em cache e invalida o cache quando dependências mudam.
    """
    def __init__(self, func, dependencies):
        self.func = func
        self.dependencies = dependencies
        self.setter_func = None
        self.deleter_func = None
        self.__doc__ = func.__doc__

    def __set_name__(self, owner, name):
        """Guarda o nome da propriedade na classe"""
        self.name = name

    def _cache_key(self):
        """Chave usada para armazenar o valor em cache"""
        return f"_{self.name}_cache"

    def _snapshot_key(self):
        """Chave usada para armazenar estado das dependencias"""
        return f"_{self.name}_snapshot"

    def _take_snapshot(self, obj):
        """Captura estado atual das dependências"""
        snapshot = {}
        for dep in self.dependencies:
            if hasattr(obj, dep):
                snapshot[dep] = getattr(obj, dep)
        return snapshot

    def _cache_is_valid(self, obj):
        """
        Verifica se o cache pode ser reutilizado comparando o estado atual
        das dependências com o anterior
        """
        cache_key = self._cache_key()
        snapshot_key = self._snapshot_key()

        if cache_key not in obj.__dict__:
            return False

        return obj.__dict__[snapshot_key] == self._take_snapshot(obj) #verifica se alguma dependencia mudou

    def __get__(self, obj, objtype=None):
        """
        Ao acessar a propriedade, retorna o valor em cache ou recalcula
        """
        if obj is None:
            return self

        if not self._cache_is_valid(obj): #verifica se cache ainda é valido (nenhuma dependência mudou)
            obj.__dict__[self._cache_key()] = self.func(obj)
            obj.__dict__[self._snapshot_key()] = self._take_snapshot(obj)

        return obj.__dict__[self._cache_key()]

    def _invalidate_cache(self, obj):
        """Remove cache armazenado"""
        obj.__dict__.pop(self._cache_key(), None)
        obj.__dict__.pop(self._snapshot_key(), None)

    def __set__(self, obj, value):
        """
        Chamado ao fazer obj.prop = valor
        Executa setter e invalida cache
        """
        if self.setter_func is None:
            raise AttributeError("can't set attribute")
        self.setter_func(obj, value)
        self._invalidate_cache(obj)

    def __delete__(self, obj):
        """
        Chaado ao fazer del obj.prop
        Executa deleter e invalida cache
        """
        if self.deleter_func is None:
            raise AttributeError("can't delete attribute")
        self.deleter_func(obj)
        self._invalidate_cache(obj)

    def setter(self, func):
        """Define função de setter"""
        self.setter_func = func
        return self

    def deleter(self, func):
        """Define função de deleter"""
        self.deleter_func = func
        return self


#testando para exemplos do exercicio
if __name__ == "__main__":
    from math import sqrt
    class Vector:
        def __init__(self, x, y, z, color=None):
            self.x, self.y, self.z = x, y, z
            self.color = color
        @computed_property('x', 'y', 'z')
        def magnitude(self):
            print('computing magnitude')
            return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    v = Vector (9,2,6)
    print(v.magnitude)
    v.color = 'red'
    print(v.magnitude)
    v.y = 18
    print(v.magnitude)

    class Circle:
        def __init__(self, radius=1):                            
            self.radius = radius
        @computed_property('radius', 'area')
        def diameter(self):
            return self.radius * 2
    circle = Circle()
    print(circle.diameter)

    class Circle:
        def __init__(self, radius=1):                            
            self.radius = radius
        @computed_property('radius', 'area')
        def diameter(self):
            return self.radius * 2
        @diameter.setter
        def diameter(self, diameter):
            self.radius = diameter / 2
        @diameter.deleter
        def diameter(self):
            self.radius = 0
    circle = Circle()
    print(circle.diameter)
    circle.diameter = 3
    print (circle.radius)
    del circle.diameter
    print(circle.radius)

    class Circle:
        def __init__(self, radius=1):
            self.radius = radius
        @computed_property('radius')
        def diameter(self):
            """Circle diameter from radius"""
            print('computing diameter')
            return self.radius * 2  
    print(help(Circle))


