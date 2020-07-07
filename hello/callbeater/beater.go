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
    cmdpkt * exec.Cmd 
}

func New() (* Callbeat)  {

    cmd := exec.Cmd {
        Path:  "/root/beats/filebeat/filebeat",
        Dir:  "/root/beats/filebeat/",
    }

    cmdpkt := exec.Cmd {
        Path:  "/root/beats/packetbeat/packetbeat",
        Dir:  "/root/beats/filebeat/",
    }

    return &Callbeat{
        started: false,
        cmd :  &cmd,
        cmdpkt : &cmdpkt,
        }
}



func (cb * Callbeat) Callfilebeat () {
    if err := cb.cmd.Start(); err != nil { 
        log.Panic(err) 
    } 
    cb.cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true} 
}


func (cb* Callbeat)   Stopfilebeat () {

    if err := cb.cmd.Process.Kill(); err != nil {
        log.Fatal("failed to kill process: ", err)
    }

    //syscall.Kill(-cb.cmd.Process.Pid, syscall.SIGKILL) 

    time.Sleep(5 * time.Second)
    fmt.Printf("stopfilebeats over\n")
}


func (cb * Callbeat) Callpacketbeat() {
    
    if err := cb.cmdpkt.Start(); err != nil {
        log.Panic(err)
    }
    cb.cmdpkt.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
    fmt.Printf("callpacketbeat\n")
}


func (cb * Callbeat) Stoppacketbeat() {

    if err := cb.cmdpkt.Process.Kill(); err != nil {
        log.Fatal("failed to kill process: ", err)
    }    

    time.Sleep(5 * time.Second)

    fmt.Printf("stoppacketbeat over\n")
}


