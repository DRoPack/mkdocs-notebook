# Expressions

## Split

```html title="Syntax"
fileName = `myFile.docx` 

split(variables('fileName'),'.')[0]
result: myFile


split(variables('fileName'),'.')[1] 
result: docx
```

Splitting a string on the n<sup>th</sup> occurrence and rejoining the string.  

```html title="Syntax"
url = `https://blotter.sharepoint.com/site/subsite`

join(take(split(variables('url'),'/'),3), '/') 

result: /site/subsite
```
