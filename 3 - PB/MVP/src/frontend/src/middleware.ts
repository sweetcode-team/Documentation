import { NextRequest, NextResponse } from 'next/server'
import { getConfiguration } from '@/app/page'

export async function middleware(req: NextRequest) {
  const pathname = req.nextUrl.pathname

  if (req.nextUrl.pathname.startsWith("/_next")) {
    return NextResponse.next();
  }

  let isConfigurationSet = false
  try {
    const currentConfiguration = await getConfiguration()
    isConfigurationSet =
      currentConfiguration.LLMModel !== null
      && currentConfiguration.documentStore !== null
      && currentConfiguration.embeddingModel !== null
      && currentConfiguration.vectorStore !== null
  } catch (error) {
    // return NextResponse.redirect(req.url, { status: 301 });
    console.error('Errore durante la richiesta:', error);
  }

  const isConfigurationPage = pathname.startsWith('/configuration')

  if (isConfigurationPage) {
    if (isConfigurationSet) {
      return NextResponse.redirect(new URL('/', req.url))
    }
    return NextResponse.next()
  }

  if (!isConfigurationSet) {
      return NextResponse.redirect(new URL('/configuration', req.url))
  }
  return NextResponse.next()
}

export const config = {
  matchter: ['/', '/chatbot', '/chatbot/:path*', '/documents', '/documents/:path*', '/settings', '/settings/:path*', '/configuration'],
}