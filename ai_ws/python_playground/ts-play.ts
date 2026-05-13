

import * as z from "zod";

const Player = z.object({
    name: z.string(),
});

interface B {
    b: string
}
interface C {
    c: string
}
type TYPE = "b" | "c"
interface A {
    type: TYPE
    b?: B
    c?: C
}

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
    id: z.number(),
    a: SchemaA
})

const Players = z.array(Player)

import yaml, { YAMLException } from "js-yaml"



function yamlZodTest(a: any) {
    // console.log(res)
    const _yaml = yaml.dump(a)
    // console.log(_yaml)
    const str = "- a: test\nb:\n -b: testestete"
    // console.log(str)
    try {
        const res = yaml.load(_yaml)

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

function _test(query: { [key: string]: string }) {

    const str = `
    {
    "properties": {
        "account": {
            "properties": {
                "name": {
                    "description": "Account Name",
                    "type": "string"
                },
                "email": {
                    "description": "Account Email",
                    "type": "string"
                },
                "country": {
                    "description": "Country",
                    "type": "string"
                }
            },
            "required": [
                "name",
                "email",
                "country"
            ],
            "type": "object",
            "description": "Account information"
        }
    },
    "required": [
        "account"
    ],
    "type": "object"
}
    `
    try {
        const res = JSON.parse(str)
        console.log(res)
    } catch (error) {
        console.log(error)
    }

}
// _test({ a: { b: { b: "werwerwe" }, c: { c: "werwerwe" } } })

const arr: string | undefined = undefined
_test({ "status": "testing" })

// _test(123123)
