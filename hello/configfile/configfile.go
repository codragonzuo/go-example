package configfile

import (
    "fmt"
    "log"
    "github.com/ghodss/yaml"
    yaml2 "gopkg.in/yaml.v2"
    "io/ioutil"
)


func Yamltojsontest() {
    t := map[string]interface{}{}
    buffer, err := ioutil.ReadFile("./config.dev.yaml")
    err = yaml2.Unmarshal(buffer, &t)
    if err != nil {
        log.Fatalf(err.Error())
    }
    fmt.Printf("%v",t)
}





func Jsontoyamltest() {

    j := []byte(`{"name": "John", "age": 30}`)
    y, err := yaml.JSONToYAML(j)
    if err != nil {
        fmt.Printf("err: %v\n", err)
        return
    }
    fmt.Println(string(y))
    /* Output:
    name: John
    age: 30
    */
    j2, err := yaml.YAMLToJSON(y)
    if err != nil {
        fmt.Printf("err: %v\n", err)
        return
    }
    fmt.Println(string(j2))
    /* Output:
    {"age":30,"name":"John"}
    */
}




