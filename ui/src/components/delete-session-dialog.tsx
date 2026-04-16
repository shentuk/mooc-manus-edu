'use client'

import {useState} from 'react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {Button} from '@/components/ui/button'

type DeleteSessionDialogProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  onConfirm: () => Promise<void>
}

/**
 * 删除任务确认弹窗
 * 确认后才发起 API 删除请求
 */
export function DeleteSessionDialog({open, onOpenChange, onConfirm}: DeleteSessionDialogProps) {
  const [deleting, setDeleting] = useState(false)

  const handleConfirm = async () => {
    setDeleting(true)
    try {
      await onConfirm()
    } finally {
      setDeleting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[440px]">
        <DialogHeader>
          <DialogTitle className="text-lg font-semibold">
            要删除任务信息吗？
          </DialogTitle>
          <DialogDescription className="text-sm text-muted-foreground leading-relaxed">
            删除任务信息后，该任务下的所有聊天记录将被永远删除，无法找回，所上传的文件与生成文件均无法查看&下载。
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button
            variant="outline"
            className="cursor-pointer"
            onClick={() => onOpenChange(false)}
            disabled={deleting}
          >
            取消
          </Button>
          <Button
            className="cursor-pointer"
            onClick={handleConfirm}
            disabled={deleting}
          >
            {deleting ? '删除中...' : '确认'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}


