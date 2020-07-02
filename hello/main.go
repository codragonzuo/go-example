package main

import (
    "fmt"
    "log"
    "github.com/codragonzuo/go-example/meal"
    "github.com/codragonzuo/go-example/hello/life"
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
)



/*
 * Tag... - a very simple struct
 */
type Tag struct {
    ID   int    `json:"id"`
    Name string `json:"name"`
}



func main() {
    meal.Getlunch()
    
    life.PrintWork()

    fmt.Println("Hello World !")

    sqlquery()
}

func sqlquery(){
    
    db, err := sql.Open("mysql", "root:qwer1234@tcp(127.0.0.1:3306)/ambari")

    // if there is an error opening the connection, handle it
    if err != nil {
        log.Print(err.Error())
        fmt.Printf("connect failed ! \n")
        return
    }
    defer db.Close()

    // Execute the query
    results, err := db.Query("SELECT user_id, user_name FROM users")
    if err != nil {
        fmt.Printf("db.query error \n")
        panic(err.Error()) // proper error handling instead of panic in your app
    }

    for results.Next() {
        var tag Tag
        // for each row, scan the result into our tag composite object
        err = results.Scan(&tag.ID, &tag.Name)
        if err != nil {
            panic(err.Error()) // proper error handling instead of panic in your app
        }
                // and then print out the tag's Name attribute
        log.Printf(tag.Name)
        fmt.Printf("%d  %s\n", tag.ID, tag.Name)
    }

}
