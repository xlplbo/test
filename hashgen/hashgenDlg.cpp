
// hashgenDlg.cpp : implementation file
//

#include "stdafx.h"
#include "hashgen.h"
#include "hashgenDlg.h"
#include "cryptohash.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	enum { IDD = IDD_ABOUTBOX };

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

// Implementation
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
END_MESSAGE_MAP()


// ChashgenDlg dialog




ChashgenDlg::ChashgenDlg(CWnd* pParent /*=NULL*/)
	: CDialog(ChashgenDlg::IDD, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void ChashgenDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(ChashgenDlg, CDialog)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	//}}AFX_MSG_MAP
   ON_BN_CLICKED(IDC_BUTTON_HASHTEXT, &ChashgenDlg::OnBnClickedButtonHashtext)
   ON_BN_CLICKED(IDC_BUTTON_HASHFILE, &ChashgenDlg::OnBnClickedButtonHashfile)
   ON_BN_CLICKED(IDC_BUTTON_BROWSE, &ChashgenDlg::OnBnClickedButtonBrowse)
END_MESSAGE_MAP()


// ChashgenDlg message handlers

BOOL ChashgenDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon

	CComboBox* pCombo = (CComboBox*)GetDlgItem(IDC_COMBO_ALGORITHM);
   ASSERT_VALID(pCombo);
   
   int pos = pCombo->AddString(_T("SHA-1"));
   pCombo->SetItemData(pos, CALG_SHA1);
   pos = pCombo->AddString(_T("MD5"));
   pCombo->SetItemData(pos, CALG_MD5);
   pos = pCombo->AddString(_T("MD4"));
   pCombo->SetItemData(pos, CALG_MD4);
   pos = pCombo->AddString(_T("MD2"));
   pCombo->SetItemData(pos, CALG_MD2);

   pCombo->SetCurSel(0);

	return TRUE;  // return TRUE  unless you set the focus to a control
}

void ChashgenDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void ChashgenDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR ChashgenDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


void ChashgenDlg::OnBnClickedButtonHashtext()
{
   CString text;
   GetDlgItemText(IDC_EDIT_TEXT, text);

   if(text.IsEmpty())
   {
      AfxMessageBox(_T("No text was introduced."));
   }

   CComboBox* pCombo = (CComboBox*)GetDlgItem(IDC_COMBO_ALGORITHM);
   ASSERT_VALID(pCombo);

   ALG_ID algorithm = (ALG_ID)pCombo->GetItemData(pCombo->GetCurSel());

   std::string hash;
   crypto::errorinfo_t lasterror;

   CT2A atext(text);
   switch(algorithm)
   {
   case CALG_SHA1:
      {
         crypto::sha1_helper_t hhelper;
         hash = hhelper.hexdigesttext(atext.m_szBuffer);
         lasterror = hhelper.lasterror();
      }
      break;
   case CALG_MD5:
      {
         crypto::md5_helper_t hhelper;
         hash = hhelper.hexdigesttext(atext.m_szBuffer);
         lasterror = hhelper.lasterror();
      }
      break;
   case CALG_MD4:
      {
         crypto::md4_helper_t hhelper;
         hash = hhelper.hexdigesttext(atext.m_szBuffer);
         lasterror = hhelper.lasterror();
      }
      break;
   case CALG_MD2:
      {
         crypto::md2_helper_t hhelper;
         hash = hhelper.hexdigesttext(atext.m_szBuffer);
         lasterror = hhelper.lasterror();
      }
      break;
   }

   if(!hash.empty())
   {
      CA2T wtext(hash.c_str());
      SetDlgItemText(IDC_EDIT_HASH, wtext.m_szBuffer);
   }
   else
   {
      CA2T wtext(lasterror.errorMessage.c_str());
      SetDlgItemText(IDC_EDIT_HASH, wtext.m_szBuffer);
   }
}

void ChashgenDlg::OnBnClickedButtonHashfile()
{
   CString filename;
   GetDlgItemText(IDC_EDIT_FILENAME, filename);

   if(filename.IsEmpty())
   {
      AfxMessageBox(_T("No filename specified!"));
      return;
   }

   DWORD attr = ::GetFileAttributes(filename);
   if(attr == INVALID_FILE_ATTRIBUTES ||
      !(((attr & FILE_ATTRIBUTE_NORMAL) == FILE_ATTRIBUTE_NORMAL) ||
      ((attr & FILE_ATTRIBUTE_ARCHIVE) == FILE_ATTRIBUTE_ARCHIVE)))
   {
      AfxMessageBox(_T("Invalid filename!"));
      return;
   }

   CComboBox* pCombo = (CComboBox*)GetDlgItem(IDC_COMBO_ALGORITHM);
   ASSERT_VALID(pCombo);

   ALG_ID algorithm = (ALG_ID)pCombo->GetItemData(pCombo->GetCurSel());

   std::string hash;
   crypto::errorinfo_t lasterror;

   CT2A afilename(filename);
   switch(algorithm)
   {
   case CALG_SHA1:
      {
         crypto::sha1_helper_t hhelper;
         hash = hhelper.hexdigestfile(afilename.m_szBuffer);
         lasterror = hhelper.lasterror();
      }
      break;
   case CALG_MD5:
      {
         crypto::md5_helper_t hhelper;
         hash = hhelper.hexdigestfile(afilename.m_szBuffer);
         lasterror = hhelper.lasterror();
      }
      break;
   case CALG_MD4:
      {
         crypto::md4_helper_t hhelper;
         hash = hhelper.hexdigestfile(afilename.m_szBuffer);
         lasterror = hhelper.lasterror();
      }
      break;
   case CALG_MD2:
      {
         crypto::md2_helper_t hhelper;
         hash = hhelper.hexdigestfile(afilename.m_szBuffer);
         lasterror = hhelper.lasterror();
      }
      break;
   }

   if(!hash.empty())
   {
      CA2T wtext(hash.c_str());
      SetDlgItemText(IDC_EDIT_HASH, wtext.m_szBuffer);
   }
   else
   {
      CA2T wtext(lasterror.errorMessage.c_str());
      SetDlgItemText(IDC_EDIT_HASH, wtext.m_szBuffer);
   }
}

void ChashgenDlg::OnBnClickedButtonBrowse()
{
   CFileDialog dlg(TRUE, NULL, NULL, 0, _T("All Files (*.*)|*.*||"), this, 0, TRUE);

   if(IDOK == dlg.DoModal())
   {
      SetDlgItemText(IDC_EDIT_FILENAME, dlg.GetPathName());
   }
}
