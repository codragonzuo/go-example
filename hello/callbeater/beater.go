package callbeater


import(
	_ "errors"
	"fmt"
        "sync"
        "os/exec"
        "log"
        "time"
        "syscall"
)




func init() {
}

// Input define a snmptrap input
type Callbeat struct {
    sync.Mutex
    started bool
    cmd  * exec.Cmd  
}

func New() (* Callbeat)  {

    cmd := exec.Cmd {
        Path:  "/root/beats/filebeat/filebeat",
        //Args: []string{"-u", "-l", "8888"},
        Dir:  "/root/beats/filebeat/",
    }


    return &Callbeat{
        started: false,
        cmd :  &cmd,
             }

}



func (cb * Callbeat) Callfilebeat () {
    if err := cb.cmd.Start(); err != nil { 
        log.Panic(err) 
    } 
    cb.cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true} 
}

func (cb* Callbeat)   Stopfilebeat () {
    //cb.cmd.Process.Kill()

    if err := cb.cmd.Process.Kill(); err != nil {
        log.Fatal("failed to kill process: ", err)
    }    //cb.cmd.Process.Kill() 
    
    //if err := cmd.Process.Kill(); err != nil {
    //    log.Fatal("failed to kill process: ", err)
    //}
    //syscall.Kill(-cb.cmd.Process.Pid, syscall.SIGKILL) 


    time.Sleep(5 * time.Second)
    fmt.Printf("stopfilebeats over\n")
}


func (cb * Callbeat) callpacketbeat() {
    fmt.Printf("callpacketbeat\n")
}


func (cb * Callbeat) stoppacketbeat() {
    fmt.Printf("stoppacketbeats\n")
}


