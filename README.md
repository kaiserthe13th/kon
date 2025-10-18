# Kaiserthe13th's Object Notation (KON)

This is an object notation format that is easily readable by a human, or machine.

## Examples

### JSON vs KON

```json
{
    "widget": {
        "debug": "on",
        "window": {
            "title": "Sample Konfabulator Widget",
            "name": "main_window",
            "width": 500,
            "height": 500
        },
        "image": { 
            "src": "Images/Sun.png",
            "name": "sun1",
            "hOffset": 250,
            "vOffset": 250,
            "alignment": "center"
        },
        "text": {
            "data": "Click Here",
            "size": 36,
            "style": "bold",
            "name": "text1",
            "hOffset": 250,
            "vOffset": 100,
            "alignment": "center",
            "onMouseUp": "sun1.opacity = (sun1.opacity / 100) * 90;"
        }
    }
}
```

```ini
widget {
    debug = on
    window {
        title = "Sample Konfabulator Widget"
        name = main_window
        width = 500
        height = 500
    }
    image { 
        src = Images/Sun.png
        name = sun1
        hOffset = 250
        vOffset = 250
        alignment = center
    }
    text {
        data = "Click Here"
        size = 36
        style = bold
        name = text1
        hOffset = 250
        vOffset = 100
        alignment = center
        onMouseUp = "sun1.opacity = (sun1.opacity / 100) * 90;"
    }
}
```

```json
{
    "glossary": {
        "title": "example glossary",
        "GlossDiv": {
            "title": "S",
            "GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986",
                    "GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                        "GlossSeeAlso": ["GML", "XML"]
                    },
                    "GlossSee": "markup"
                }
            }
        }
    }
}
```

```ini
glossary {
    title = "example glossary"
    GlossDiv {
        title = S
        GlossList {
            GlossEntry {
                ID = SGML
                SortAs = SGML
                GlossTerm = "Standard Generalized Markup Language"
                Acronym = SGML
                Abbrev = "ISO 8879:1986"
                GlossDef {
                    para = "A meta-markup language, used to create markup languages such as DocBook."
                    GlossSeeAlso(GML, XML)
                }
                GlossSee = markup
            }
        }
    }
}
```

```json
{
    "menu": {
        "header": "SVG Viewer",
        "items": [
            {"id": "Open"},
            {"id": "OpenNew", "label": "Open New"},
            null,
            {"id": "ZoomIn", "label": "Zoom In"},
            {"id": "ZoomOut", "label": "Zoom Out"},
            {"id": "OriginalView", "label": "Original View"},
            null,
            {"id": "Quality"},
            {"id": "Pause"},
            {"id": "Mute"},
            null,
            {"id": "Find", "label": "Find..."},
            {"id": "FindAgain", "label": "Find Again"},
            {"id": "Copy"},
            {"id": "CopyAgain", "label": "Copy Again"},
            {"id": "CopySVG", "label": "Copy SVG"},
            {"id": "ViewSVG", "label": "View SVG"},
            {"id": "ViewSource", "label": "View Source"},
            {"id": "SaveAs", "label": "Save As"},
            null,
            {"id": "Help"},
            {"id": "About", "label": "About Adobe CVG Viewer..."}
        ]
    }
}
```

```ini
menu {
    header = "SVG Viewer",
    items(
        { id = Open }
        { id = OpenNew, label = "Open New" }
        null
        { id = ZoomIn, label = "Zoom In" }
        { id = ZoomOut, label = "Zoom Out" }
        { id = OriginalView, label = "Original View" }
        null
        { id = Quality }
        { id = Pause }
        { id = Mute }
        null
        { id = Find, label = "Find..." }
        { id = FindAgain, label = "Find Again" }
        { id = Copy }
        { id = CopyAgain, label = "Copy Again" }
        { id = CopySVG, label = "Copy SVG" }
        { id = ViewSVG, label = "View SVG" }
        { id = ViewSource, label = "View Source" }
        { id = SaveAs, label = "Save As" }
        null
        { id = Help }
        { id = About, label = "About Adobe CVG Viewer..." }
    )
}
```
