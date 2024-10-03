
# Libs
`pip install GoogleNews` <br/>
`pip install datetime` <br/>
`pip install timedelta` <br/>
`pip install Flask`


# Como executar
- <b> flask -app webapp.py run </b>



## Noticias do dia

 - GET /api/news/{company}/today


## Noticias em um período

 - GET /api/news/{company}?start={date}&end={date}


#### Retorno esperado

```
[
    [
        {
            "date": string,
            "datetime": datetime,
            "desc": string,
            "img": string,
            "link": string,
            "media": string,
            "reporter": string,
            "site": string,
            "title": string
        }
    ]
]
```