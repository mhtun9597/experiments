'use client'
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { ChangeEvent, forwardRef, useEffect, useRef, useState } from "react";
import { io, Socket } from "socket.io-client";
import { useVal } from "../hooks/play";

const API_BASE = "http://localhost:3333/api"

interface SampleResponse {
    msg: string;
    status: boolean;
    dt: Date;
    data: any
}


const Page: React.FC = () => {

    const queryClient = useQueryClient()
    const [socket, setSocket] = useState<Socket>()
    const [connected, setConnected] = useState<boolean>(false)
    const inputRef = useRef<HTMLInputElement>(null)


    const [s1, setS1] = useState(0)
    const v = useVal(s1)

    useEffect(() => {
        const _socket: Socket = io('ws://localhost:3333/ns1')
        setSocket(_socket)

        _socket.on("my_event", (msg, ack) => {
            // console.log("Room Event Received ", msg)
            // ack(true)
        })
        _socket.on("room_event", (msg, ack) => {
            // console.log("Room Event Received ", msg)
            // ack(true)
        })
        _socket.on("connect", () => {
            // console.log("Socket connected", _socket.id)
            // _socket.emit("enter_room", "1")
            // _socket.emit()
            setConnected(true)
        })
        _socket.on("disconnect", () => {
            // console.log("Socket disconnected")
            setConnected(false)

        })
        _socket.on("connect_error", () => {
            console.log("Socket Connect Error")
            setConnected(false)

        })

        return () => {
            if (socket && socket.connected) {
                socket.disconnect()
            }
        }
    }, [])
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
        setS1((prev) => { return prev + 1 })

    }
    const [input, setInput] = useState("")
    const handlerrr = (event: ChangeEvent<HTMLInputElement, HTMLInputElement>) => {
        event.preventDefault()
        console.log("value ", event.target.value)
        setInput(event.target.value)
    }
    return <div>
        <span>{state1}</span>
        <button style={{ border: "1px solid black" }} onClick={handleClick} >Send</button>
        <span>Status :: {status}</span>
        <span>Error :: {error?.message}</span>
        <span>Data :: {data ? data.msg : "12312321"}</span>
        <span>{v}</span>
        <span>{s1}</span>
        <input style={{ border: "1px solid black" }} type="text" value={input} onChange={handlerrr}></input>
        <div style={{ padding: "2px" }}><p>{input}</p></div>

    </div>
}

type DivProps = React.HTMLAttributes<HTMLDivElement> & {
    children?: React.ReactNode;
};
export const Box = forwardRef<HTMLDivElement, DivProps>(
    ({ children, ...props }, ref) => {
        return (
            <div ref={ref} {...props}>
                {children}
            </div>
        );
    }
);

Box.displayName = "Box";


export default Page