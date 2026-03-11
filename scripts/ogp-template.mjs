/**
 * OGP画像のオーバーレイテンプレート（satori用）
 * テンプレート画像の上にタイトルとタグを配置する
 */

export const OGP_WIDTH = 1200;
export const OGP_HEIGHT = 630;
export const MAX_TAGS = 4;

/**
 * タイトル・タグオーバーレイ用のテンプレートを生成
 * @param {Object} options
 * @param {string} options.title - 記事タイトル
 * @param {string[]} options.tags - タグ配列（最大4つ）
 * @returns {Object} satori用のJSX-likeオブジェクト
 */
export function createOverlayTemplate({ title, tags = [] }) {
  const displayTags = tags.slice(0, MAX_TAGS);

  return {
    type: 'div',
    props: {
      style: {
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-start',
        paddingTop: '100px',
        paddingLeft: '80px',
        paddingRight: '80px',
        fontFamily: 'Latin, JP',
      },
      children: [
        // タイトル
        {
          type: 'div',
          props: {
            style: {
              display: 'flex',
              maxWidth: '1080px',
            },
            children: {
              type: 'span',
              props: {
                style: {
                  color: '#1a1a1a',
                  fontSize: '48px',
                  lineHeight: 1.4,
                  wordBreak: 'break-word',
                },
                children: title,
              },
            },
          },
        },
        // タグ
        ...(displayTags.length > 0
          ? [
              {
                type: 'div',
                props: {
                  style: {
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '16px',
                    marginTop: '20px',
                  },
                  children: displayTags.map((tag) => ({
                    type: 'span',
                    props: {
                      style: {
                        color: '#4a9ece',
                        fontSize: '20px',
                        fontFamily: 'Latin, JP',
                      },
                      children: `#${tag}`,
                    },
                  })),
                },
              },
            ]
          : []),
      ],
    },
  };
}
