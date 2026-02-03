'use client'
import { useQuery } from "@tanstack/react-query";
import { ChangeEvent, useEffect, useRef, useState } from "react";
import { io, Socket } from "socket.io-client";

const API_BASE = "http://localhost:3333/api"

interface SampleResponse {
    msg: string;
    status: boolean;
    dt: Date;
    data: any
}


const Page: React.FC = () => {


    // const [socket, setSocket] = useState<Socket>()
    const inputRef = useRef<HTMLInputElement>(null)

    // useEffect(() => {
    //     const _socket: Socket = io('ws://localhost:3333/ns1')
    //     setSocket(_socket)

    //     _socket.on("my_event", (msg, ack) => {
    //         console.log("Room Event Received ", msg)
    //         ack(true)
    //     })
    //     _socket.on("room_event", (msg, ack) => {
    //         console.log("Room Event Received ", msg)
    //         ack(true)
    //     })
    //     _socket.on("connect", () => {
    //         console.log("Socket connected", _socket.id)
    //         _socket.emit("enter_room", "1")
    //         // _socket.emit()
    //     })
    //     _socket.on("disconnect", () => {
    //         console.log("Socket disconnected")

    //     })
    //     _socket.on("connect_error", () => {
    //         console.log("Socket Connect Error")

    //     })

    //     return () => {
    //         if (socket && socket.connected) {
    //             socket.disconnect()
    //         }
    //     }
    // }, [])
    const fetchCount = async (): Promise<SampleResponse> => {
        const response = await fetch(API_BASE)
        console.log("Response => ", response)
        if (!response.ok) {

            throw new Error('Network response was not ok')

        }
        return response.json()
    }
    const { status, data, error } = useQuery({
        queryKey: ['test'],
        queryFn: fetchCount,
    })




    const [state, setState] = useState(() => {
        console.log("date state initialized")
        return new Date()
    })
    const [state1, setState1] = useState(1)


    const handleClick = () => {

        // if (!inputRef.current || !socket || !socket.connected) return
        // const msg = inputRef.current.value
        // socket.emit("room_event", "1")
        setState1(new Date().getTime())

    }
    return <div>
        <span>{state1}</span><input ref={inputRef} style={{ border: "1px solid black" }}></input>
        <button style={{ border: "1px solid black" }} onClick={handleClick} >Send</button>
        <span>Status :: {status}</span>
        <span>Error :: {error?.message}</span>
        <span>Data :: {data ? data.msg : "12312321"}</span>

    </div>
}



export default Page