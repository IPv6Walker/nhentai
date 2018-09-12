About nhentai.sh
===

run `bash nhentai.sh`, and you will get several albums from [nhentai.net](https://nhentai.net) in manga directory.

Prerequist
---

1. python > 3;
2. python package: [requests,bs4,re];
3. [aria2](https://aria2.github.io/);

More options
---

| command | usage
|-|-
| --data_dir | Name a directory to store the downloaded albums: `bash nhentai.sh --data_dir nico-robin`
| --search | Input search string(muti-strings should be connected by +) for resources in nhnetai: `bash nhentai.sh --search nico+robin`
