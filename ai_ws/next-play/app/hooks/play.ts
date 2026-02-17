import { useEffect, useState } from "react"

export const useVal = (v: number) => {

    const [val, setVal] = useState(`val_${v}`)


    useEffect(() => {
        setVal(`val_${v}`)
    }, [v])
    return val
}