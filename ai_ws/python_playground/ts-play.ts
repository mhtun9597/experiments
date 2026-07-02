

import * as z from "zod";

const Player = z.object({
    name: z.string(),
});


type TYPE = "b" | "c"

interface T {
    id: number,
    a: A
}

const SchemaB = z.object({ b: z.string() })
const SchemaC = z.object({ c: z.string() })
const SchemaA = z.discriminatedUnion("type", [
    z.object({
        type: z.literal("b"),
        b: SchemaB,
    }), // Allows extra keys for type 'b'
    z.object({
        type: z.literal("c"),
        c: SchemaC,
    }) // Allows extra keys for type 'c'
]);

const SchemaT = z.object({
    id: z.string().refine((val) => !/\s/.test(val), {
        message: "No whitespace allowed",
    }),
})

const Players = z.array(Player)

import yaml, { YAMLException } from "js-yaml"



function yamlZodTest() {
    // console.log(res)
    // const _yaml = yaml.dump(a)
    // console.log(_yaml)
    // const str = "- a: test\nb:\n -b: testestete"
    // console.log(str)
    try {
        // const res = yaml.load(_yaml)
        const res = { "id": "dassad sadsa" }

        const validation = SchemaT.parse(res)
    } catch (error) {
        if (error instanceof YAMLException) {
            console.log(error.cause)
            console.log(error.mark)

            console.log(error.message)

            console.log(error.name)

            console.log(error.reason)
            console.log(error.stack)

        } else if (error instanceof z.ZodError) {

            const err = JSON.parse(error.message)
            console.log("ZOD Error ", err)
        } else {
            console.log("Common Error ", String(error))

        }
    }

}

interface IT {
    id: number
}

interface A {
    a?: string
    b?: string
}
interface B {
    b: string
}

interface C {
    c: A & B
}
import { v4 as uuidv4 } from 'uuid';

function _test() {
    let a = ""
    
}
_test()



// yamlZodTest()
// _test({ a: { b: { b: "werwerwe" }, c: { c: "werwerwe" } } })

// const arr: string | undefined = undefined
// _test({ "status": "testing" })

// _test(123123)

// interface A {
//     a: "a"
// }
// function __test(v: any) {

//     let arr = [1, 2, 3, 4]
//     arr.splice(1, 1)
//     console.log(arr)

// }

// __test({ "b": "b", "a": "a" })