'use client'
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { ChangeEvent, forwardRef, useEffect, useMemo, useRef, useState } from "react";
import { io, Socket } from "socket.io-client";
import { useVal } from "../hooks/play";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

const API_BASE = "http://localhost:3333/api"

const fetchExample = async (): Promise<number> => {
    console.log("fetched")
    return new Date().valueOf()

}


const Page: React.FC = () => {
    const searchParams = useSearchParams()

    const [count, setCount] = useState<number>()

    const { data: _count } = useQuery({
        queryKey: ["tests", { count: count }],
        queryFn: fetchExample,
        enabled: count != undefined
    })

    const handlClick = () => {
        setCount(prev => { return (prev || 0) + 1 })
    }


    // const handlClick = () => {
    //     const params = new URLSearchParams(searchParams.toString());

    //     params.set("count", (count ? Number(count) + 1 : 1).toString())
    //     router.push(`${pathname}?${params.toString()}`);

    // }


    return <div>
        Testing
        <span>{count}</span>
        <button onClick={handlClick}>Click</button>
        <button onClick={() => { setCount(undefined) }}>Rest</button>

    </div>
}


export default Page