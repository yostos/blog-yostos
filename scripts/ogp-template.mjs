/**
 * OGP画像のテンプレート（satori用）
 * デフォルト背景画像にタイトル等をオーバーレイする
 */

/**
 * タイトルオーバーレイ用のテンプレートを生成
 * @param {Object} options
 * @param {string} options.title - 記事タイトル
 * @param {string} options.author - 著者名
 * @param {string} options.blogName - ブログ名
 * @returns {Object} satori用のJSX-likeオブジェクト
 */
export function createOverlayTemplate({ title, author, blogName }) {
  return {
    type: 'div',
    props: {
      style: {
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        padding: '40px',
        fontFamily: 'Latin, JP',
      },
      children: [
        // ブログ名（左上）
        {
          type: 'div',
          props: {
            style: {
              display: 'flex',
              justifyContent: 'flex-start',
            },
            children: {
              type: 'span',
              props: {
                style: {
                  color: 'white',
                  fontSize: '28px',
                  fontWeight: 'bold',
                  textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)',
                },
                children: blogName,
              },
            },
          },
        },
        // 下部コンテナ（タイトル + 著者名）
        {
          type: 'div',
          props: {
            style: {
              display: 'flex',
              flexDirection: 'column',
            },
            children: [
              // タイトル部分（半透明背景ボックス付き）
              {
                type: 'div',
                props: {
                  style: {
                    display: 'flex',
                    backgroundColor: 'rgba(0, 0, 0, 0.6)',
                    borderRadius: '12px',
                    padding: '24px 32px',
                    marginBottom: '20px',
                    maxWidth: '90%',
                  },
                  children: {
                    type: 'span',
                    props: {
                      style: {
                        color: 'white',
                        fontSize: '42px',
                        fontWeight: 'normal',
                        lineHeight: 1.4,
                        wordBreak: 'break-word',
                      },
                      children: title,
                    },
                  },
                },
              },
              // 著者名（右下）
              {
                type: 'div',
                props: {
                  style: {
                    display: 'flex',
                    justifyContent: 'flex-end',
                    width: '100%',
                  },
                  children: {
                    type: 'span',
                    props: {
                      style: {
                        color: 'white',
                        fontSize: '24px',
                        opacity: 0.9,
                        textShadow: '1px 1px 2px rgba(0, 0, 0, 0.5)',
                      },
                      children: author,
                    },
                  },
                },
              },
            ],
          },
        },
      ],
    },
  };
}

export const OGP_WIDTH = 1200;
export const OGP_HEIGHT = 630;
export const DEFAULT_AUTHOR = 'Toshiyuki Yoshida';
export const BLOG_NAME = 'Coded Chords';
