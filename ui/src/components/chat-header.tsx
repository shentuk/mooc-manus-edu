'use client'

import Link from 'next/link'
import {SidebarTrigger, useSidebar} from '@/components/ui/sidebar'
import {ManusSettings} from '@/components/manus-settings'

export function ChatHeader() {
  const {open, isMobile} = useSidebar()

  return (
    <header className="flex justify-between items-center w-full py-2 px-4 z-50">
      {/* 左侧操作&logo */}
      <div className="flex items-center gap-2">
        {/* 面板操作按钮: 关闭面板&移动端下会显示 */}
        {(!open || isMobile) && <SidebarTrigger className="cursor-pointer"/>}
        {/* EduManus Logo */}
        <Link href="/" className="flex items-center gap-2 h-9 px-3 rounded-md bg-white hover:bg-gray-50 transition-colors">
          <div className="flex items-center justify-center w-6 h-6 rounded-md bg-gradient-to-br from-blue-500 to-emerald-500">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 3L1 9L5 11.18V17.18L12 21L19 17.18V11.18L21 10.09V17H23V9L12 3ZM18.82 9L12 12.72L5.18 9L12 5.28L18.82 9ZM17 15.99L12 18.72L7 15.99V12.27L12 15L17 12.27V15.99Z" fill="white"/>
            </svg>
          </div>
          <span className="text-sm font-semibold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-emerald-600">EduManus</span>
        </Link>
      </div>
      {/* 右侧设置模态窗 */}
      <ManusSettings/>
    </header>
  )
}