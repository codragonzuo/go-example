package callbeater


import(
	_ "errors"
	"fmt"
        "sync"
)




func init() {
}

// Input define a snmptrap input
type Callbeater struct {
	sync.Mutex
	started bool
}



func (cb * Callbeater)callbeats(){
     fmt.Printf("callbeats\n")

}


func (cb * Callbeater)  callfilebeat () {

    fmt.Printf("callfilebeats\n")

}


func (cb * Callbeater)   stopfilebeat () {

    fmt.Printf("stopfilebeats\n")


}


func (cb * Callbeater) callpacketbeat() {
    fmt.Printf("callpacketbeat\n")
}


func (cb * Callbeater) stoppacketbeat() {
    fmt.Printf("stoppacketbeats\n")
}












