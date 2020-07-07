package main

import (
    "fmt"
    "log"
    "runtime"
    "github.com/codragonzuo/go-example/meal"
    "github.com/codragonzuo/go-example/hello/life"
    "github.com/codragonzuo/go-example/hello/rpcserver"
    _ "github.com/codragonzuo/go-example/commu/commu"
    _ "github.com/codragonzuo/go-example/commu/sharedlib"
    "github.com/apache/thrift/lib/go/thrift"
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

    //go say ("world")
    //say ("hello")
    //sqlquery()


    runserver()
}

func sayhello(){
    say ("hello")
    sqlquery()

}

func say(s string){
    //for  {
    for i:=0; i<5; i++ {
        runtime.Gosched()
        fmt.Println(s)
    }
}




func runserver(){
       var protocolFactory thrift.TProtocolFactory
       var transportFactory thrift.TTransportFactory

	//compact
	protocolFactory = thrift.NewTCompactProtocolFactory()
	//simplejson
	//protocolFactory = thrift.NewTSimpleJSONProtocolFactory()
	//case "json":
	protocolFactory = thrift.NewTJSONProtocolFactory()
	//case "binary", "":
	//protocolFactory = thrift.NewTBinaryProtocolFactoryDefault()

	//buffered
	transportFactory = thrift.NewTBufferedTransportFactory(8192)
	//} else {
	//transportFactory = thrift.NewTTransportFactory()
	
	//framed
        //transportFactory = thrift.NewTFramedTransportFactory(transportFactory)

        if err := rpcserver.RunServer(transportFactory, protocolFactory, "192.168.20.45:8091", false); err != nil {
			fmt.Println("error running server:", err)
        }

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
    results, err := db.Query("select alert_id ,alert_label from alert_history where alert_id > 8840")
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
