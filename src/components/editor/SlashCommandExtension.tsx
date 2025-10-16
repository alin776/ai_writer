/**
 * Slash 命令扩展
 */
import { Extension } from '@tiptap/core';
import { ReactRenderer } from '@tiptap/react';
import Suggestion from '@tiptap/suggestion';
import { SlashCommandsMenu, slashCommands, filterCommands, type CommandItem } from './SlashCommands';
import tippy, { Instance as TippyInstance } from 'tippy.js';

export const SlashCommand = Extension.create({
  name: 'slashCommand',

  addOptions() {
    return {
      suggestion: {
        char: '/',
        startOfLine: false,
        command: ({ editor, range, props }: any) => {
          props.command(editor);
          editor.chain().focus().deleteRange(range).run();
        },
      },
    };
  },

  addProseMirrorPlugins() {
    return [
      Suggestion({
        editor: this.editor,
        ...this.options.suggestion,

        items: ({ query }: { query: string }) => {
          return filterCommands(query);
        },

        render: () => {
          let component: ReactRenderer;
          let popup: TippyInstance[];

          return {
            onStart: (props: any) => {
              component = new ReactRenderer(SlashCommandsMenu, {
                props: {
                  items: props.items,
                  selectedIndex: 0,
                  onSelect: (index: number) => {
                    const item = props.items[index];
                    if (item) {
                      props.command(item);
                    }
                  },
                },
                editor: props.editor,
              });

              if (!props.clientRect) {
                return;
              }

              popup = tippy('body', {
                getReferenceClientRect: props.clientRect,
                appendTo: () => document.body,
                content: component.element,
                showOnCreate: true,
                interactive: true,
                trigger: 'manual',
                placement: 'bottom-start',
                theme: 'slash-commands',
                maxWidth: 'none',
              });
            },

            onUpdate(props: any) {
              component.updateProps({
                items: props.items,
                selectedIndex: props.selectedIndex || 0,
              });

              if (!props.clientRect) {
                return;
              }

              popup[0]?.setProps({
                getReferenceClientRect: props.clientRect,
              });
            },

            onKeyDown(props: any) {
              if (props.event.key === 'Escape') {
                popup[0]?.hide();
                return true;
              }

              if (props.event.key === 'ArrowUp') {
                const newIndex = props.selectedIndex === 0
                  ? props.items.length - 1
                  : props.selectedIndex - 1;

                component.updateProps({
                  selectedIndex: newIndex,
                });
                return true;
              }

              if (props.event.key === 'ArrowDown') {
                const newIndex = props.selectedIndex === props.items.length - 1
                  ? 0
                  : props.selectedIndex + 1;

                component.updateProps({
                  selectedIndex: newIndex,
                });
                return true;
              }

              if (props.event.key === 'Enter') {
                const item = props.items[props.selectedIndex];
                if (item) {
                  props.command(item);
                }
                return true;
              }

              return false;
            },

            onExit() {
              popup[0]?.destroy();
              component.destroy();
            },
          };
        },
      }),
    ];
  },
});
