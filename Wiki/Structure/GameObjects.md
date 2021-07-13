Es gibt 2 grosse Arten von Gameobjects.
- Static GameObjects
- Dynamic GameObjects (`DynamicObject`)

Dabei unterscheiden sich beide darin, das Static GameObjects keinen Code
besitzen. Dynamic GameObjects schon.

Die Dynamic GameObjects basieren auf dem Panda3d Actor, welches ermöglicht auch
Animationen einspielen zu lassen.

Alle GameObjects werden in einem Array `objectRegistry` in der Application
Instanz gespeichert. Von dort aus kann dann auf die Objekte zugegriffen werden.

Ein grosser Unterschied zwischen Dynamic GameObjects und Static GameObjects ist,
dass die Static GameObjects gleich das Node Component das Objekt ist. Bei den
Dynamic GameObjects ist es so, dass es noch ein unter Node, die `visNode` gibt,
welches für die Animation und das aussehen verantwortlich ist.
