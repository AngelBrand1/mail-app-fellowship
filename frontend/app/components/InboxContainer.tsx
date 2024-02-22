'use client'
import { useEffect, type ReactElement, useState } from "react"
import { InboxCard } from "./InboxCard"
import emailsData  from "@/public/testEmails.json"
import { Email } from "../types/EmailInterface"
export interface InboxContainerProps {
  
}

export function InboxContainer(props: InboxContainerProps): ReactElement {
  const [choosed, setChoosed] = useState<number>(1)
  const emails: Email[] = JSON.parse(JSON.stringify(emailsData))
  console.log(emails)
  return (
    <section className="w-1/4 min-w-96 ">
      {emails.map(( email, index ) => (
        <InboxCard key={email.id} {...email} choosed={choosed} setChoosed={setChoosed}/>
      ))}

    </section>
  )
}
