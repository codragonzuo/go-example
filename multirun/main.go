package main

import (
    "fmt"
    "log"
//    "runtime"
    "os"
    "os/signal"
    "os/exec"
    "time"
    "sync"
    "syscall"
    _"io/ioutil"
)

func main() {
    fmt.Println("Hello World !")

    cb := NewCallbeat()
    
    //stdin, _  := cb.cmdzoo.StdinPipe()
    //stdout, _ := cb.cmdzoo.StdoutPipe()
    
    cb.CallZookeeper()

    fmt.Println("call zookeeper ...")
    
    time.Sleep(10 * time.Second)
    

    
    /*go func() { 
        if err := cb.cmdzoo.Wait(); err != nil { 
            fmt.Printf("Child process %d exit with err: %v\n", cb.cmdzoo.Process.Pid, err) 
        } 
    }() */
    
    cb.CallKafka()
    fmt.Println("call kafka ...")
    cb.CallSnort()
    fmt.Println("call snort ...")
    cb.CallFilebeat()
    fmt.Println("call filebeat ...")
    /*
    go func() { 
        if err := cb.cmdkafka.Wait(); err != nil { 
            fmt.Printf("Child process %d exit with err: %v\n", cb.cmdkafka.Process.Pid, err) 
        } 
    }() */
    c := make(chan os.Signal, 1) 
    signal.Notify(c, os.Interrupt) 
    s := <-c 
    
    //out_bytes, _ := ioutil.ReadAll(stdout)
    //stdout.Close()
    //fmt.Println("Execute finished:" + string(out_bytes))    
    fmt.Println("Got signal:", s) 

}

type Callbeat struct {
    sync.Mutex
    started bool
    cmdzoo  * exec.Cmd 
    cmdkafka * exec.Cmd
    cmdsnort * exec.Cmd
    cmdfilebeat * exec.Cmd
    cmdflink * exec.Cmd
    cmdsecevent  * exec.Cmd
}

func NewCallbeat() (* Callbeat)  {

    cmdzoo := exec.Cmd {
        Path:  "/root/kafka_2.11-2.1.0/bin/zookeeper-server-start.sh",
        Args: []string{"-daemon","zookeeper.properties"}, 
        Dir:  "/root/kafka_2.11-2.1.0/config/",
    }

    cmdkafka := exec.Cmd {
        Path:  "/root/kafka_2.11-2.1.0/bin/kafka-server-start.sh",
        Args: []string{"-daemon","/root/kafka_2.11-2.1.0/config/server.properties"}, 
        Dir:  "/root/kafka_2.11-2.1.0/bin/",
    }
    
    cmdfilebeat := exec.Cmd {
        Path:  "/root/beats/filebeat/filebeat",
        //Args: []string{}, 
        Dir:  "/root/beats/filebeat/",
    }

    cmdsnort := exec.Cmd {
        Path:  "/usr/local/bin/snort",
        Args: []string{"-v -c snort.conf -i eth1 -y -U"}, 
        Dir:  "/etc/snort",
    }

    return &Callbeat{
        started: false,
        cmdzoo :  &cmdzoo,
        cmdkafka : &cmdkafka,
        cmdsnort: &cmdsnort,
        cmdfilebeat: &cmdfilebeat,
        }
}

func (cb * Callbeat) CallZookeeper () {
    if err := cb.cmdzoo.Start(); err != nil { 
        log.Panic(err) 
    } 
    cb.cmdzoo.SysProcAttr = &syscall.SysProcAttr{Setpgid: true} 

    fmt.Println("Start child process with pid", cb.cmdzoo.Process.Pid) 
}

func (cb * Callbeat) CallKafka() {
    if err := cb.cmdkafka.Start(); err != nil {
        log.Panic(err)
    }
    cb.cmdkafka.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}

    fmt.Println("Start child process with pid", cb.cmdkafka.Process.Pid)
}

func (cb * Callbeat) CallSnort() {
    if err := cb.cmdsnort.Start(); err != nil {
        log.Panic(err)
    }
    cb.cmdsnort.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}

    fmt.Println("Start child process with pid", cb.cmdsnort.Process.Pid)
}

func (cb * Callbeat) CallFilebeat() {
    if err := cb.cmdfilebeat.Start(); err != nil {
        log.Panic(err)
    }
    cb.cmdfilebeat.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}

    fmt.Println("Start child process with pid", cb.cmdfilebeat.Process.Pid)
}
