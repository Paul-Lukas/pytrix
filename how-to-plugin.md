# How to write a Plugin

## Struktur
Alle Plugins bestehen aus einem Ordner, welcher wie das Plugin benannt ist. Dieser Ordner wird samt aller Dateien, am Ende in den plugin Ordner von pytrix importiert.
Des Weiteren besteht jedes Plugin aus der eigentlichen Plugin-Datei "Pluginname".py

Die Struktur sollte dann so aussehen (Pluginname = testris) :

- testris
	+ testris.py

Diese Struktur ist das, was unbedingt benötigt wird.
Sie kann nach Belieben mit Dateien und Ordnern erweitert werden.

## Die Plugin-Datei
Die Plugin-Datei (hier testris.py) besteht aus einer Klasse, auch diese ist nach dem Plugin benannt und erbt von der BasePlugin Klasse, zu finden unter `pytrix/src/plugins/basePlugin.py`

Wenn ihr euer erstes Plugin für pytrix programmiert, empfehle ich, als allererstes das folgende Grundgerüst zu kopieren ("Testris" ist entsprechend durch den eigenen Pluginnamen zu ersetzen, wie auch die version).

### Grundgerüst:
```python
from ..basePlugin import BasePlugin


class Testris(BasePlugin):
    def __init__(self, app, output):
        super().__init__(app, output)
        self.pluginName = "Testris"
        self.version = "pre 0.1"

    def run(self):
		pass

    def input(self, inp):
        pass

	def get_html(self):
		pass
```

### Was macht was?
#### Der super Konstruktor: 
Das Grundgerüst besteht im Wesentlichen aus dem super Konstruktor:
```python
 super().__init__(app, output)
```
dieser stellt im Wesentlichen zwei Variablen bereit:
|Variablen Name| Funktion |
|--|--|
| self.out | Output (Später genauer beschrieben) |
| self.app | Für fortgeschrittene Funktionen |

---

#### Die init Methode:
Ist eine in Python eingebaute Methode, sie wird beim Laden des Plugins (beim Starten von pytrix) ausgeführt.
In dieser Methode dürfen aller höchstens Variablen definiert werden.

---

#### Die Run Methode:
Ist der Einstiegspunkt des Plugins, sie wird ausgeführt, sobald das Plugin auf der Website mittels des Start-Buttons gestartet wird.
Der Return Wert wird aktuell noch nicht verwendet, könnte später aber einmal auf der Website angezeigt werden.

---

#### Die Input Methode:
Wird aufgerufen, wenn auf eurer jeweiligen plugin URL ein Input ankommt. Der Input wird als Dict Objekt mittels variable inp übergeben.
Die inp variable wird immer aus den mittels GET übergebenen Parametern erstellt. Die GET Parameter `?name_des_inputs=2` können wie folgt ausgelesen werden:
```python
input_var = inp.get("name_des_inputs")
```
Die Variable "input_var" enthält entsprechend "2" (wichtig, als String)

Die Input Methode muss keinen Return Wert liefern. (Dieser kann von euch aber theoretisch später mittels JavaScript genutzt werden, was allerdings nur für Fortgeschrittene ist, dar etwas kompliziert).

---

#### Die get_html Methode:
Wird beim Auswählen des Plugins (vor dem Starten, also vor der Run Methode) aufgerufen. Ihr Return wert sollte eine Website beinhalten und wird auf der Website angezeigt. Dieser Return wert, diese Website bildet eure eigentliche Eingabe. Hier **müssen alle Inputfelder definiert** werden. Mehr dazu im folgenden Abschnitt Input.

---
---
### Wie muss meine Website aussehen?
Die Input-Seite, besteht immer aus HTML und JavaScript, CSS ist optional, aber empfohlen.

#### Was sind die Aufgaben der Website?
Die Website bildet den Input eures Programms. Sie wird einmal über die get_html Methode geladen. Ab dann müssen Inputs des Benutzers und wenn benötigt auch Outputs via JavaScript an das Plugin weitergeleitet werden.
Jedes Plugin hat eine eigene URL, die Inputs, die über GET-Parameter an diese Adresse gelangen, werden an die jeweilige Input-Methode weiter geleitet

---

#### Technisches
Beim Rendern der Website werden bestimmte Platzhalter ersetzt. 
(Wer es genau wissen möchte, die Website wird mit der Jinja template engine gerendert)

| Platzhalter Name | Funktion |
|--|--|
| start_name | Der Name des gestarteten Plugins (sprich der Name des Plugins, welcher in der Klasse angegeben wird) |
| start_id | Die ID des gestarteten Plugins

*Hinweis: es gibt noch mehr Platzhalter, welche allerdings für die Plugins nicht relevant sein sollten*

> Exkurs die Plugin ID:
> 
> die Plugin ID ist etwas, was immer wieder aufkommt, anhand von ihr passiert fast alles im Bezug auf Plugins:
>  - Plugin Namen werden der Klasse zugeordnet
>  - Die Inputs werden den Plugins zugeordnet
>  - Das zu startende Plugin wird ausgewählt
>  - etc.
>  
>  Das Konzept der Plugin ID ist also wirklich wichtig, ohne sie funktioniert gar nichts. Glücklicher weiße funktioniert die meiste zuordnung im Hintergrund und ist für den Plugin Entwickler nur beim Senden der Inputs Relevant.
>  
>  (Die ID ist übrigens fortlaufend und wird beim Start von pytrix, um genau zu sein, beim erstellen der Plugin Liste, generiert. Sie kann sich bei jedem Start ändern)

Die oben beschriebenen Platzhalter werden innerhalb des HTML wie folgt verwendet:

    <p> {{ start_name }} </p>
    wird zu -> <p> Testris </p>

*Dasselbe gilt auch für start_id*
Die Platzhalter können in der kompletten Datei verwendet werden, sie werden praktisch einfach gesucht und ersetzt.

---

#### Senden von Inputs
Um einen Input von der Website zum Plugin zu bekommen, muss er als GET Request an eine bestimmte URL.
Diese URL setzt sich wie folgt zusammen `/plugin/"plugin id"/input?"GET Parameter"`

Beispiel:
Möchte man den Parameter namens "input_blah" mit dem Wert 123 an das Plugin schicken, so kann die URL auf der Website wie folgt geschrieben werden.

    /plugin/{{ start_id }}/input?input_blah=123

Das GET Request an diese URL kann in **JavaScript** wie folgt gesendet werden
```javascript
var xmlHttp = new XMLHttpRequest();
xmlHttp.open( "GET", "/plugin/{{ start_id }}/input?input_blah=123", false ); // false for synchronous
xmlHttp.send( null );
```

---

#### Beispiel für eine Website:
*Das Beispiel sind Auszüge aus dem Start-Button, wie er zum Starten der Plugins verwendet wird*

```html
<h1 onclick="startPlugin()">START PLUGIN: {{ start_name }}</h1>

<script>
function startPlugin() {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open( "GET", "/plugin/-1/input?start_id={{ start_id }}", false ); // false for synchronous request
	xmlHttp.send( null );
}
</script>
```

In diesem Beispiel gibt einen klickbaren Text (h1). Das Attribut "onclick" kann auf praktisch alles angewendet werden und sorgt dafür, dass der Browser beim Klicken (eben onclick) die angegebene JavaScript-Funktion ausführt.

Das Script ist praktisch das gleiche, wie eben schon gesehen, das einzig neue ist die Funktion, in der alles steht. Diese wird eben beim Klicken ausgeführt. Den Inhalt der Funktion ist oben schon ausführlich beschrieben, für einen einfachen Input (ohne Bestätigung oder sonstige Rückgabe) ist nur die URL von Interesse.


---
---
## Wie bekomme ich Pixel auf das Board
Mit der Variable `self.out` können Pixel auf dem Board angezeigt werden.
Mit der Variable wird eine Klasse übergeben (welche wird nach den Einstellungen in der Config entschieden).
Alle Klassen besitzen folgende Methoden, welche von dem Plugin benutzt werden müssen:

| Methode | Parameter | Funktion | Beispiel |
|--|--|--|--|
| fill_all | -Farbe als Tupel mit 3 werten (r, g, b) 0-254 | Setzt der ganze Bord auf die angegebene Farbe | `self.out.fill_all((0, 0, 0))` |
| out[x, y] | Koordinaten | Setzt einen Pixel | `self.out[0, 0] = (0, 0, 0)` |
| submit_all | - | Überträgt die Änderungen | `self.out.submit_all()` |
| set_matrix | -Matrix (2 dimensional Array of Tupels) | setzt die ganze Matrix | `self.matrix.out(testMatrix)` |

