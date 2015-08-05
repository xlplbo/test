
// hashgenDlg.h : header file
//

#pragma once


// ChashgenDlg dialog
class ChashgenDlg : public CDialog
{
// Construction
public:
	ChashgenDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	enum { IDD = IDD_HASHGEN_DIALOG };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support


// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
   afx_msg void OnBnClickedButtonHashtext();
   afx_msg void OnBnClickedButtonHashfile();
   afx_msg void OnBnClickedButtonBrowse();
};
