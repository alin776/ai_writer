Unexpected Application Error!
Cannot read properties of undefined (reading 'getTime')
TypeError: Cannot read properties of undefined (reading 'getTime')
    at formatRelativeTime (http://localhost:5173/src/utils/formatDate.ts:13:61)
    at http://localhost:5173/src/views/AdminInvitationsView/index.tsx:564:100
    at Array.map (<anonymous>)
    at AdminInvitationsView (http://localhost:5173/src/views/AdminInvitationsView/index.tsx:498:32)
    at Object.react_stack_bottom_frame (http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=335500c6:18509:20)
    at renderWithHooks (http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=335500c6:5654:24)
    at updateFunctionComponent (http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=335500c6:7475:21)
    at beginWork (http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=335500c6:8525:20)
    at runWithFiberInDEV (http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=335500c6:997:72)
    at performUnitOfWork (http://localhost:5173/node_modules/.vite/deps/react-dom_client.js?v=335500c6:12561:98)
💿 Hey developer 👋

You can provide a way better UX than this when your app throws errors by providing your own ErrorBoundary or errorElement prop on your route.