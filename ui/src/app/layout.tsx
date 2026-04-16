import React from 'react'
import type {Metadata} from 'next'
import {SidebarProvider} from '@/components/ui/sidebar'
import {SessionsProvider} from '@/providers/sessions-provider'
import {Toaster} from '@/components/ui/sonner'
import './globals.css'
import {LeftPanel} from '@/components/left-panel'

export const metadata: Metadata = {
  title: 'EduManus - 教学智能体协作系统',
  description: 'EduManus 是一个面向教学领域的多智能体协作系统，支持课程规划、作业批改、答疑辅导、学习分析和试题生成等教学场景，助力教师高效教学。',
  icons: {
    icon: '/icon.png',
  },
}

export default function RootLayout(
  {
    children,
  }: Readonly<{
    children: React.ReactNode;
  }>,
) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
    <body className="h-screen overflow-hidden">
    <SessionsProvider>
      <SidebarProvider
        style={{
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-expect-error
          '--sidebar-width': '300px',
          '--sidebar-width-icon': '300px',
        }}
      >
        {/* 左侧的面板 */}
        <LeftPanel/>
        {/* 右侧的内容 */}
        <div className="flex-1 bg-[#f8f8f7] h-screen overflow-hidden">
          {children}
        </div>
      </SidebarProvider>
    </SessionsProvider>
    <Toaster position="top-center" richColors/>
    </body>
    </html>
  )
}