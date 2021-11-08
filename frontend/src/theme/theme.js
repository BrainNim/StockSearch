import { css } from 'styled-components';

const flexSpaceBetween = css`
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
`;

const flexAlignItemsCenter = css`
  display: flex;
  align-items: center;
`;
const flexCenter = css`
  display: flex;
  justify-content: center;
  align-items: center;
`;
const flexColumn = css`
  display: flex;
  flex-direction: column;
  width: 100%;
`;

const skeletonStyles = css`
  background-color: #d6d6d6;
  border-radius: 0.4rem;
`;

const theme = {
  fontFamily: 'Noto Sans KR',
  fontWeight: {
    normal: '400',
    bold: '700',
    bold2: '900',
  },
  color: {
    default: '#A590EF',
    modalBackground: '#020000',
    purple: '#703DE4',
    gray: 'rgba(0, 0, 0, 0.44)',
    grayLine: 'rgba(0, 0, 0, 0.26)',
    yellow: '#FFE661',
    whitePurple: '#F4F0FF',
  },
  fontSize: {
    XXL: '2rem', // 32px
    XL: '1.5rem', //  24px
    L: '1.2rem', //18px
    M: '1rem', // 16px
    S: '0.75rem', //12px
  },

  border: {
    radius: {
      XL: '2rem', // 30px
      L: '1.25rem', // 20px
      M: '1rem', // 16px
      S: '0.7rem', // 11px
    },
  },
  style: {
    flexColumn: `${flexColumn}`,
    flexSpaceBetween: `${flexSpaceBetween}`,
    flexAlignItemsCenter: `${flexAlignItemsCenter}`,
    flexCenter: `${flexCenter}`,
    skeletonStyles: `${skeletonStyles}`,
  },
};

export default theme;
