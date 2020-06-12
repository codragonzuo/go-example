## Go Package Example



### 修改 ./git/config,这样git才能提交
```
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[remote "origin"]
        fetch = +refs/heads/*:refs/remotes/origin/*
#       url = https://github.com/codragonzuo/go-example.git
        url = ssh://git@github.com/codragonzuo/go-example.git

[branch "master"]
        remote = origin
        merge = refs/heads/master
```

### go run main.go运行hello/main.go
