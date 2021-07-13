Es gibt 2 grosse Arten von Gameobjects.
- Static GameObjects
- Dynamic GameObjects (`DynamicObject`)

Dabei unterscheiden sich beide darin, das Static GameObjects keinen Code
besitzen. Dynamic GameObjects schon.

Alle GameObjects werden in einem Array `objectRegistry` in der Application
Instanz gespeichert. Von dort aus kann dann auf die Objekte zugegriffen werden.
