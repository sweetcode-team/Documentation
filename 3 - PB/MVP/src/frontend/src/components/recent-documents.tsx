"use client";
import { formatDate, formatDistanceToNow } from "date-fns";
import { cn } from "@/lib/utils"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Button } from "@/components/ui/button"

import { LightDocument } from "@/types/types"
import { DOCUMENT_STATUSES } from "@/constants/constants"

import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer"

import {
  Table,
  TableBody,
  TableCell,
  TableRow,
} from "@/components/ui/table"

import Link from "next/link";
import prettyBytes from "pretty-bytes";
import { StatusBadge } from "./status-badge";
import { useEffect, useState } from "react";

interface RecentDocumentsProps {
  items: LightDocument[]
}

async function getDocumentContent(id: string): Promise<LightDocument> {
  const result = await fetch(`http://localhost:4000/getDocumentContent/${id}`)
  return result.json()
}

// export async function handleClick(id: string) {
//   const [src, setSrc] = useState('');

//   useEffect(() => {
//     const documentContent = await getDocumentContent("2024-02-19.pdf");
//     const prova = Buffer.from(documentContent.content, 'hex')
//     const blob = new Blob([prova], { type: 'application/pdf' });
//     //Object.assign(prova, {preview:  URL.createObjectURL(blob)});
//     const pdfUrl = URL.createObjectURL(blob);
//     setSrc(pdfUrl);
//   }, [documentContent.content]);

//   return (
//     <div>
//       <a href={src} target="_blank"> prova </a>
//     </div>
//   );
// }

export function RecentDocuments({ items }: RecentDocumentsProps) {

  return (
    <ScrollArea>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 m-2">
        {items.map((item) => (
          <Drawer key={item.id}>
            <DrawerTrigger asChild>
              <div
                className={cn(
                  "flex flex-col items-start gap-1 rounded-lg border p-3 text-left text-sm transition-all hover:bg-accent w-full",
                )}
              >
                <div className="w-full min-w-0">
                  <p className="font-semibold truncate">{item.id}</p>
                </div>
                <div className="flex flex-col md:flex-row w-full items-center justify-between gap-2">
                  <div className="text-xs line-clamp-1">{prettyBytes(item.size)} | {item.type.toUpperCase()}</div>
                  {
                    item.status &&
                    <StatusBadge
                      className="truncate"
                      variant={DOCUMENT_STATUSES.find(
                        (status) => status.value === item.status
                      )?.style as any}>
                      <span className="truncate">{DOCUMENT_STATUSES.find(
                        (status) => status.value === item.status
                      )?.label}</span>
                    </StatusBadge>
                  }
                </div>
              </div>
            </DrawerTrigger>
            <DrawerContent className="max-h-screen">
              <div className="mx-auto w-full sm:w-6/12 xl:w-4/12 max-h-screen overflow-auto">
                <DrawerHeader className="pb-0">
                  <DrawerTitle className="text-wrap break-all">{item.id}</DrawerTitle>
                  <DrawerDescription>Document details.</DrawerDescription>
                </DrawerHeader>
                <div className="px-4 pb-0 xl:py-4 w-full">
                  <Table className="mt-3">
                    <TableBody>
                      <TableRow>
                        <TableCell className="font-bold">Type</TableCell>
                        <TableCell>{item.type}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell className="font-bold">Dimension</TableCell>
                        <TableCell>{prettyBytes(item.size)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell className="font-bold">Upload time</TableCell>
                        <TableCell>
                          {
                            formatDate(item.uploadTime, "dd MMM yyyy HH:mm")
                          }
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell className="font-bold">Status</TableCell>
                        <TableCell>
                          {
                            item.status &&
                            <StatusBadge
                              variant={DOCUMENT_STATUSES.find(
                                (status) => status.value === item.status
                              )?.style as any}>
                              <span className="truncate">{item.status}</span>
                            </StatusBadge>
                          }
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </div>
                <DrawerFooter>
                  <Button asChild>
                    <Link href={`/documents/${item.id}`} >
                      View content
                    </Link>
                  </Button>
                  <DrawerClose asChild>
                    <Button variant="outline">Close</Button>
                  </DrawerClose>
                </DrawerFooter>
              </div>
            </DrawerContent>
          </Drawer>
        ))}
      </div>
    </ScrollArea >
  )
}