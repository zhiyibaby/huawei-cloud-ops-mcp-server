from playwright.sync_api import sync_playwright, Page, Browser
import time
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import json
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Index,
    UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

huawei_urls = {
    'ecs': {
        'url': 'https://www.huaweicloud.com/pricing/calculator.html#/ecs',
        'labels': [
            '区域', '可用区', 'CPU架构', '规格', '镜像', '规格价格'
        ]
    }
}

# 全局数据结构，用于存储所有收集的信息
ecs_price_data = {
    'regions': []  # 区域列表，每个区域包含可用区、CPU架构等信息
}


def setup_browser(playwright) -> Tuple[Browser, Page]:
    """设置浏览器和页面"""
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # 设置对话框自动处理
    def handle_dialog(dialog):
        print(f"检测到对话框: {dialog.type} - {dialog.message}")
        dialog.dismiss()

    page.on("dialog", handle_dialog)

    # 设置超时时间
    page.set_default_timeout(60000)
    page.set_default_navigation_timeout(60000)

    return browser, page


def navigate_to_page(page: Page, url: str) -> None:
    """导航到指定页面"""
    print(f"正在访问: {url}")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        print("页面已加载")
    except Exception as e:
        print(f"页面加载失败: {e}")
        page.goto(url, wait_until="commit", timeout=60000)
        print("页面导航已提交")

    # 等待页面完全加载
    print("等待页面完全加载...")
    time.sleep(3)


def close_popups(page: Page) -> None:
    """关闭页面弹窗"""
    print("正在处理页面弹窗...")
    popup_selectors = [
        'button[aria-label*="关闭"]',
        'button[aria-label*="close"]',
        'button[aria-label*="Close"]',
        '[class*="close"]',
        '[class*="modal-close"]',
        '[class*="popup-close"]',
        'button:has-text("关闭")',
        'button:has-text("×")',
        'button:has-text("我知道了")',
        'button:has-text("同意")',
        'button:has-text("确定")',
    ]

    for selector in popup_selectors:
        try:
            elements = page.locator(selector).all()
            for element in elements:
                if element.is_visible(timeout=1000):
                    print(f"找到弹窗关闭按钮: {selector}")
                    element.click()
                    time.sleep(0.5)
                    break
        except Exception:
            continue

    # 尝试按 ESC 键关闭弹窗
    try:
        page.keyboard.press("Escape")
        time.sleep(0.5)
    except Exception:
        pass

    time.sleep(1)
    print("弹窗处理完成")


def click_price_detail(page: Page) -> bool:
    """点击价格详情按钮"""
    print("\n正在查找并点击价格详情按钮...")
    price_detail_selectors = [
        'text=价格详情',
        'button:has-text("价格详情")',
        'a:has-text("价格详情")',
        '[class*="price"]:has-text("价格详情")',
        '[class*="detail"]:has-text("价格详情")',
        'button:has-text("详情")',
    ]

    for selector in price_detail_selectors:
        try:
            element = page.locator(selector).first
            if element.is_visible(timeout=3000):
                print(f"找到价格详情按钮: {selector}")
                element.scroll_into_view_if_needed()
                time.sleep(0.5)
                element.click(timeout=3000)
                print("✓ 已点击价格详情按钮")
                return True
        except Exception:
            continue

    print("✗ 未找到价格详情按钮，尝试截图查看页面结构...")
    page.screenshot(path="page_screenshot_before_price_detail.png")
    print("已保存截图到 page_screenshot_before_price_detail.png")
    return False


def find_label_by_text(page: Page, label_text: str) -> Optional[any]:
    """查找完全匹配指定文本的label元素"""
    print(f"\n正在查找完全匹配label '{label_text}'...")

    label_selectors = [
        f'label:has-text("{label_text}")',
        f'label:text-is("{label_text}")',
    ]

    for selector in label_selectors:
        try:
            elements = page.locator(selector).all()
            for element in elements:
                if element.is_visible(timeout=3000):
                    text = element.inner_text().strip()
                    # 完全匹配
                    if text == label_text:
                        print(f"找到label元素: {selector}, 文本: '{text}'")
                        return element
        except Exception:
            continue

    # 如果还没找到，尝试更精确的查找
    try:
        all_labels = page.locator('label').all()
        for label in all_labels:
            try:
                if label.is_visible(timeout=1000):
                    text = label.inner_text().strip()
                    if text == label_text:
                        print(f"找到label元素（精确匹配）: '{label_text}'")
                        return label
            except Exception:
                continue
    except Exception:
        pass

    print(f"✗ 未找到完全匹配'{label_text}'的label元素")
    return None


def find_region_label(page: Page) -> Optional[any]:
    """查找完全匹配'区域'的label元素"""
    return find_label_by_text(page, "区域")


def find_zone_label(page: Page) -> Optional[any]:
    """查找完全匹配'可用区'的label元素"""
    return find_label_by_text(page, "可用区")


def find_cpu_arch_label(page: Page) -> Optional[any]:
    """查找完全匹配'CPU架构'的label元素"""
    return find_label_by_text(page, "CPU架构")


def find_spec_label(page: Page) -> Optional[any]:
    """查找完全匹配'规格'的label元素"""
    return find_label_by_text(page, "规格")


def find_image_label(page: Page) -> Optional[any]:
    """查找完全匹配'镜像'的label元素"""
    return find_label_by_text(page, "镜像")


def find_buttons_below_label_js(
    page: Page, label_element: any, label_text: str
) -> List[any]:
    """使用JavaScript查找label同级别下面的button"""
    print(f"使用JavaScript查找{label_text}同级别下面的button...")
    buttons_js = page.evaluate(f"""
        () => {{
            // 找到完全匹配"{label_text}"的label元素
            const labels = Array.from(
                document.querySelectorAll('label')
            );
            let labelEl = null;
            for (const label of labels) {{
                const text = label.textContent.trim();
                if (text === '{label_text}') {{
                    labelEl = label;
                    break;
                }}
            }}
            if (!labelEl) return [];

            const labelParent = labelEl.parentElement;
            if (!labelParent) return [];

            // 获取同一父容器下、在label后面的所有button
            const allButtons = Array.from(
                labelParent.querySelectorAll('button')
            );
            const buttonsBelow = [];

            for (const btn of allButtons) {{
                // 检查button是否可见
                const rect = btn.getBoundingClientRect();
                if (rect.width === 0 &&
                    rect.height === 0) continue;

                // 检查button是否在label之后（DOM顺序）
                const labelPos = labelEl
                    .compareDocumentPosition(btn);
                const afterLabel = (
                    labelPos &
                    Node.DOCUMENT_POSITION_FOLLOWING
                ) !== 0;

                // 检查button是否在同一父容器下
                let btnParent = btn.parentElement;
                let isSameParent = false;
                while (btnParent &&
                       btnParent !== document.body) {{
                    if (btnParent === labelParent) {{
                        isSameParent = true;
                        break;
                    }}
                    btnParent = btnParent.parentElement;
                }}

                // 如果button在label之后且在同一父容器下
                if (afterLabel && isSameParent) {{
                    buttonsBelow.push(btn);
                }}
            }}

            return buttonsBelow.map(btn => ({{
                text: btn.textContent.trim(),
                selector: btn.getAttribute('class') ||
                          btn.tagName
            }}));
        }}
    """)

    buttons = []
    if buttons_js:
        print(f"JavaScript方法找到 {len(buttons_js)} 个button")
        # 根据文本重新定位这些button
        for btn_info in buttons_js:
            try:
                btn_text = btn_info['text']
                if btn_text:
                    btn = page.locator(
                        f'button:has-text("{btn_text}")'
                    ).first
                    if btn.is_visible(timeout=1000):
                        buttons.append(btn)
            except Exception:
                continue

    return buttons


def find_buttons_below_label_playwright(
    page: Page, label_element: any, label_text: str
) -> List[any]:
    """使用Playwright查找label同级别下面的button"""
    print(f"尝试使用Playwright查找{label_text}同级别下面的button...")
    buttons = []

    try:
        # 查找label的后续兄弟button
        sibling_buttons = label_element.locator(
            'xpath=following-sibling::button'
        ).all()
        for btn in sibling_buttons:
            try:
                if btn.is_visible(timeout=500):
                    buttons.append(btn)
            except Exception:
                continue

        # 如果还没找到，查找父容器下、在label之后的button
        if not buttons:
            parent = label_element.locator('xpath=..')
            parent_buttons = parent.locator('button').all()
            label_box = label_element.bounding_box()
            if label_box:
                for btn in parent_buttons:
                    try:
                        if btn.is_visible(timeout=500):
                            btn_box = btn.bounding_box()
                            if btn_box:
                                # 检查button是否在label下方
                                btn_y = btn_box['y']
                                label_y = (
                                    label_box['y'] +
                                    label_box['height']
                                )
                                if btn_y >= label_y:
                                    buttons.append(btn)
                    except Exception:
                        continue

        if buttons:
            print(f"Playwright方法成功: 找到 {len(buttons)} 个button")
    except Exception as e:
        print(f"Playwright方法执行出错: {e}")

    return buttons


def find_buttons_below_label(
    page: Page, label_element: any, label_text: str
) -> List[any]:
    """查找label同级别下面的所有button"""
    print(f"\n正在获取{label_text}同级别下面的button...")
    buttons = []

    if not label_element:
        return buttons

    try:
        # 首先尝试JavaScript方法
        buttons = find_buttons_below_label_js(
            page, label_element, label_text
        )

        # 如果JavaScript方法没找到，使用Playwright查找
        if not buttons:
            buttons = find_buttons_below_label_playwright(
                page, label_element, label_text
            )
    except Exception as e:
        print(f"查找{label_text}同级别下面的button时出错: {e}")
        import traceback
        traceback.print_exc()

    return buttons


def find_buttons_below_region_js(page: Page, region_element: any) -> List[any]:
    """使用JavaScript查找区域下面的button"""
    return find_buttons_below_label_js(page, region_element, "区域")


def find_buttons_below_region_playwright(
    page: Page, region_element: any
) -> List[any]:
    """使用Playwright查找区域下面的button"""
    return find_buttons_below_label_playwright(page, region_element, "区域")


def find_buttons_below_region(page: Page, region_element: any) -> List[any]:
    """查找区域下面的所有button"""
    return find_buttons_below_label(page, region_element, "区域")


def filter_valid_buttons(buttons: List[any]) -> List[Dict]:
    """过滤和去重button"""
    button_texts = set()
    valid_buttons = []

    for btn in buttons:
        try:
            # 检查元素是否可见
            if not btn.is_visible(timeout=500):
                continue
            text = btn.inner_text().strip()
            # 过滤掉空文本和明显不是区域选项的文本
            if text and text not in button_texts and len(text) > 0:
                # 区域选项通常包含中文字符或连字符
                has_chinese = any(
                    '\u4e00' <= c <= '\u9fff' for c in text
                )
                if has_chinese or '-' in text or len(text) < 50:
                    button_texts.add(text)
                    valid_buttons.append({
                        'element': btn,
                        'text': text
                    })
        except Exception:
            continue

    return valid_buttons


def click_zone_buttons(
    page: Page, url_type: Optional[str] = None
) -> List[Dict]:
    """查找并点击可用区同级别下的所有button，返回可用区数据"""
    print("\n  [可用区] 开始查找可用区label...")
    zone_label = find_zone_label(page)

    if not zone_label:
        print("  [可用区] ✗ 未找到可用区label，跳过")
        return []

    # 查找可用区同级别下的button
    zone_buttons = find_buttons_below_label(page, zone_label, "可用区")

    if not zone_buttons:
        print("  [可用区] ✗ 未找到可用区同级别下的button")
        return []

    # 过滤和去重
    valid_zone_buttons = filter_valid_buttons(zone_buttons)

    if not valid_zone_buttons:
        print("  [可用区] ✗ 未找到有效的可用区button")
        return []

    print(f"  [可用区] 找到 {len(valid_zone_buttons)} 个可用区button:")
    for i, btn_info in enumerate(valid_zone_buttons, 1):
        print(f"    {i}. {btn_info['text']}")

    zones_data = []  # 存储所有可用区数据

    # 点击所有可用区button
    print(f"  [可用区] 开始点击可用区button（共 {len(valid_zone_buttons)} 个）...")
    for i, btn_info in enumerate(valid_zone_buttons, 1):
        try:
            btn_text = btn_info['text']
            total = len(valid_zone_buttons)
            print(f"  [可用区] [{i}/{total}] 正在点击: {btn_text}")

            btn_element = btn_info['element']

            # 滚动到元素可见
            btn_element.scroll_into_view_if_needed()
            time.sleep(0.5)

            # 点击button
            if btn_element.is_visible(timeout=2000):
                btn_element.click(timeout=2000)
                print(f"    ✓ 已点击: {btn_text}")
            else:
                print(f"    ✗ button不可见: {btn_text}")
                continue

            # 等待页面响应
            time.sleep(1)

            # 点击可用区button后，查找并点击CPU架构button
            cpu_archs_data = click_cpu_arch_buttons(page, url_type)
            if cpu_archs_data:
                zones_data.append({
                    'zone': btn_text,
                    'cpu_archs': cpu_archs_data
                })
            else:
                # 如果没有CPU架构数据，至少记录可用区名称
                zones_data.append({
                    'zone': btn_text,
                    'cpu_archs': []
                })

        except Exception as e:
            print(f"    ✗ 点击button '{btn_text}' 时出错: {e}")
            continue

    print(f"  [可用区] ✓ 已完成所有可用区button的点击（共 {len(valid_zone_buttons)} 个）")
    return zones_data


def click_cpu_arch_buttons(
    page: Page, url_type: Optional[str] = None
) -> List[Dict]:
    """查找并点击CPU架构同级别下的所有button，返回CPU架构数据"""
    print("\n    [CPU架构] 开始查找CPU架构label...")
    cpu_arch_label = find_cpu_arch_label(page)

    if not cpu_arch_label:
        print("    [CPU架构] ✗ 未找到CPU架构label，跳过")
        return []

    # 查找CPU架构同级别下的button
    cpu_arch_buttons = find_buttons_below_label(
        page, cpu_arch_label, "CPU架构"
    )

    if not cpu_arch_buttons:
        print("    [CPU架构] ✗ 未找到CPU架构同级别下的button")
        return []

    # 过滤和去重
    valid_cpu_arch_buttons = filter_valid_buttons(cpu_arch_buttons)

    if not valid_cpu_arch_buttons:
        print("    [CPU架构] ✗ 未找到有效的CPU架构button")
        return []

    print(f"    [CPU架构] 找到 {len(valid_cpu_arch_buttons)} 个CPU架构button:")
    for i, btn_info in enumerate(valid_cpu_arch_buttons, 1):
        print(f"      {i}. {btn_info['text']}")

    cpu_archs_data = []  # 存储所有CPU架构数据

    # 点击所有CPU架构button
    print(
        f"    [CPU架构] 开始点击CPU架构button"
        f"（共 {len(valid_cpu_arch_buttons)} 个）..."
    )
    for i, btn_info in enumerate(valid_cpu_arch_buttons, 1):
        try:
            btn_text = btn_info['text']
            total = len(valid_cpu_arch_buttons)
            print(f"    [CPU架构] [{i}/{total}] 正在点击: {btn_text}")

            btn_element = btn_info['element']

            # 滚动到元素可见
            btn_element.scroll_into_view_if_needed()
            time.sleep(0.5)

            # 点击button
            if btn_element.is_visible(timeout=2000):
                btn_element.click(timeout=2000)
                print(f"      ✓ 已点击: {btn_text}")
            else:
                print(f"      ✗ button不可见: {btn_text}")
                continue

            # 等待页面响应
            time.sleep(1)

            # 点击CPU架构button后，查找并点击规格button
            specs_data = click_spec_buttons(page, url_type)
            if specs_data:
                cpu_archs_data.append({
                    'cpu_arch': btn_text,
                    'specs': specs_data
                })
            else:
                # 如果没有规格数据，至少记录CPU架构名称
                cpu_archs_data.append({
                    'cpu_arch': btn_text,
                    'specs': []
                })

        except Exception as e:
            print(f"      ✗ 点击button '{btn_text}' 时出错: {e}")
            continue

    print(
        f"    [CPU架构] ✓ 已完成所有CPU架构button的点击"
        f"（共 {len(valid_cpu_arch_buttons)} 个）"
    )
    return cpu_archs_data


def find_and_click_buttons_in_sibling_divs(
    page: Page, spec_label: any
) -> List[Dict]:
    """通过id找到priceDetail_ecs_flavor_table容器，然后找到第三个div并
    点击其中的button，返回规格和镜像数据"""
    print(
        "\n      [规格-第三个div] 开始查找"
        "priceDetail_ecs_flavor_table的第三个div..."
    )

    specs_data = []  # 存储所有规格及其镜像数据

    try:
        # 使用JavaScript通过id找到父容器，然后找到第三个div
        result = page.evaluate("""
            () => {
                // 直接通过id找到父级容器
                const parentContainer = document.getElementById(
                    'priceDetail_ecs_flavor_table'
                );
                if (!parentContainer) {
                    console.log('未找到id为priceDetail_ecs_flavor_table的容器');
                    return null;
                }

                // 找到父容器下的所有直接子div（按DOM顺序）
                const allDivs = Array.from(parentContainer.children).filter(
                    child => child.tagName === 'DIV'
                );

                console.log('父容器ID:', parentContainer.id);
                console.log('所有div数量:', allDivs.length);

                // 找到第三个div（索引为2）
                if (allDivs.length < 3) {
                    console.log('div数量不足3个，当前数量:', allDivs.length);
                    return {
                        parentContainerId: parentContainer.id || '',
                        parentContainerClass: parentContainer.className || '',
                        totalDivs: allDivs.length,
                        targetDivIndex: 2,
                        buttons: []
                    };
                }

                const targetDiv = allDivs[2];  // 第三个div，索引为2
                console.log('找到第三个div，索引:', 2);

                // 在第三个div下查找button
                const buttons = [];
                const divButtons = Array.from(
                    targetDiv.querySelectorAll('button')
                );
                for (const btn of divButtons) {
                    // 检查button是否可见
                    const rect = btn.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        const btnText = btn.textContent.trim();
                        if (btnText) {  // 只添加有文本的button
                            // 生成XPath用于精确定位
                            function getXPath(element) {
                                if (element.id !== '') {
                                    return '//*[@id="' + element.id + '"]';
                                }
                                if (element === document.body) {
                                    return '/html/body';
                                }
                                let ix = 0;
                                const siblings = element.parentNode.childNodes;
                                for (let i = 0; i < siblings.length; i++) {
                                    const sibling = siblings[i];
                                    if (sibling === element) {
                                        return getXPath(element.parentNode) +
                                            '/' +
                                            element.tagName.toLowerCase() +
                                            '[' + (ix + 1) + ']';
                                    }
                                    if (sibling.nodeType === 1 &&
                                        sibling.tagName === element.tagName) {
                                        ix++;
                                    }
                                }
                            }

                            buttons.push({
                                text: btnText,
                                className: btn.className || '',
                                id: btn.id || '',
                                xpath: getXPath(btn),
                                index: buttons.length  // 在div中的索引
                            });
                        }
                    }
                }

                console.log('在第三个div中找到button数量:', buttons.length);

                return {
                    parentContainerId: parentContainer.id || '',
                    parentContainerClass: parentContainer.className || '',
                    totalDivs: allDivs.length,
                    targetDivIndex: 2,
                    buttons: buttons
                };
            }
        """)

        if not result:
            print("      [规格-第三个div] ✗ 未找到父容器priceDetail_ecs_flavor_table")
            return

        buttons_info = result.get('buttons', [])
        if not buttons_info:
            print("      [规格-第三个div] ✗ 未找到button")
            print(f"      父容器ID: {result.get('parentContainerId', '')}")
            print(f"      父容器Class: {result.get('parentContainerClass', '')}")
            print(f"      目标div索引: {result.get('targetDivIndex', -1)}")
            print(f"      总div数量: {result.get('totalDivs', 0)}")
            return

        print(f"      [规格-第三个div] 找到 {len(buttons_info)} 个button")
        print(f"      父容器ID: {result.get('parentContainerId', '')}")
        print(f"      目标div索引: {result.get('targetDivIndex', -1)} (第三个div)")
        print(f"      总div数量: {result.get('totalDivs', 0)}")

        # 点击找到的button
        for i, btn_info in enumerate(buttons_info, 1):
            try:
                btn_text = btn_info.get('text', '')
                if not btn_text:
                    continue

                total = len(buttons_info)
                print(
                    f"      [规格-第三个div] [{i}/{total}] "
                    f"正在点击: {btn_text}"
                )

                # 优先使用XPath定位，如果不行则使用在第三个div内定位
                btn_element = None
                xpath = btn_info.get('xpath', '')

                if xpath:
                    try:
                        btn_element = page.locator(f'xpath={xpath}').first
                        if not btn_element.is_visible(timeout=1000):
                            btn_element = None
                    except Exception:
                        btn_element = None

                # 如果XPath定位失败，尝试在第三个div内定位
                if not btn_element:
                    try:
                        # 在第三个div内查找button
                        target_div = page.locator(
                            '#priceDetail_ecs_flavor_table > div'
                        ).nth(2)  # 第三个div，索引为2
                        btn_element = target_div.locator(
                            f'button:has-text("{btn_text}")'
                        ).first
                    except Exception:
                        btn_element = None

                # 如果还是失败，使用全局文本定位
                if not btn_element:
                    btn_element = page.locator(
                        f'button:has-text("{btn_text}")'
                    ).first

                # 尝试点击button
                try:
                    if btn_element.is_visible(timeout=2000):
                        btn_element.scroll_into_view_if_needed()
                        time.sleep(0.5)
                        btn_element.click(timeout=2000)
                        print(f"        ✓ 已点击: {btn_text}")
                        time.sleep(1)

                        # 点击规格button后，等待页面更新，然后查找并点击镜像
                        # 同级别div下的button
                        time.sleep(1.5)  # 等待页面更新
                        images_data = (
                            find_and_click_buttons_in_image_sibling_divs(page)
                        )
                        if images_data:
                            specs_data.append({
                                'spec': btn_text,
                                'images': images_data
                            })
                    else:
                        # 如果不可见，尝试使用JavaScript直接点击
                        print(
                            f"        [尝试JS点击] button不可见，"
                            f"尝试使用JavaScript点击: {btn_text}"
                        )
                        clicked = page.evaluate(f"""
                            () => {{
                                const container = document.getElementById(
                                    'priceDetail_ecs_flavor_table'
                                );
                                if (!container) return false;
                                const divs = Array.from(container.children)
                                    .filter(c => c.tagName === 'DIV');
                                if (divs.length < 3) return false;
                                const targetDiv = divs[2];
                                const buttons = Array.from(
                                    targetDiv.querySelectorAll('button')
                                );
                                for (const btn of buttons) {{
                                    const btnText = btn.textContent.trim();
                                    if (btnText === '{btn_text}') {{
                                        const rect =
                                            btn.getBoundingClientRect();
                                        if (rect.width > 0 &&
                                            rect.height > 0) {{
                                            btn.scrollIntoView(
                                                {{block: 'center'}}
                                            );
                                            btn.click();
                                            return true;
                                        }}
                                    }}
                                }}
                                return false;
                            }}
                        """)
                        if clicked:
                            print(
                                f"        ✓ 已通过JavaScript点击: {btn_text}"
                            )
                            time.sleep(1.5)
                            images_data = (
                                find_and_click_buttons_in_image_sibling_divs(
                                    page
                                )
                            )
                            if images_data:
                                specs_data.append({
                                    'spec': btn_text,
                                    'images': images_data
                                })
                        else:
                            print(f"        ✗ button不可见且JS点击失败: {btn_text}")
                except Exception as e:
                    print(f"        ✗ 点击button '{btn_text}' 时出错: {e}")
                    # 尝试使用JavaScript点击
                    try:
                        clicked = page.evaluate(f"""
                            () => {{
                                const container = document.getElementById(
                                    'priceDetail_ecs_flavor_table'
                                );
                                if (!container) return false;
                                const divs = Array.from(container.children)
                                    .filter(c => c.tagName === 'DIV');
                                if (divs.length < 3) return false;
                                const targetDiv = divs[2];
                                const buttons = Array.from(
                                    targetDiv.querySelectorAll('button')
                                );
                                for (const btn of buttons) {{
                                    const btnText = btn.textContent.trim();
                                    if (btnText === '{btn_text}') {{
                                        btn.scrollIntoView(
                                            {{block: 'center'}}
                                        );
                                        btn.click();
                                        return true;
                                    }}
                                }}
                                return false;
                            }}
                        """)
                        if clicked:
                            print(
                                f"        ✓ 已通过JavaScript点击: {btn_text}"
                            )
                            time.sleep(1.5)
                            images_data = (
                                find_and_click_buttons_in_image_sibling_divs(
                                    page
                                )
                            )
                            if images_data:
                                specs_data.append({
                                    'spec': btn_text,
                                    'images': images_data
                                })
                    except Exception:
                        pass

            except Exception as e:
                btn_text = btn_info.get('text', '')
                print(f"        ✗ 点击button '{btn_text}' 时出错: {e}")
                continue

        print(
            f"      [规格-第三个div] ✓ 已完成所有button的点击"
            f"（共 {len(buttons_info)} 个）"
        )
        return specs_data

    except Exception as e:
        print(f"      [规格-第三个div] ✗ 查找第三个div时出错: {e}")
        import traceback
        traceback.print_exc()
        return specs_data


def find_and_click_buttons_in_image_sibling_divs(
    page: Page
) -> List[Dict]:
    """通过id找到priceDetail_ecs_image_table容器，然后查找并点击其中的
    button，返回镜像和价格数据"""
    print("\n        [镜像] 开始查找priceDetail_ecs_image_table中的button...")

    # 等待页面更新，确保镜像容器已经出现
    time.sleep(1)

    images_data = []  # 存储所有镜像及其价格数据

    try:
        # 使用JavaScript通过id找到父容器，然后查找其中的button
        result = page.evaluate("""
            () => {
                // 直接通过id找到父级容器
                const parentContainer = document.getElementById(
                    'priceDetail_ecs_image_table'
                );
                if (!parentContainer) {
                    console.log('未找到id为priceDetail_ecs_image_table的容器');
                    return null;
                }

                console.log('父容器ID:', parentContainer.id);

                // 在容器下查找所有button
                const buttons = [];
                const allButtons = Array.from(
                    parentContainer.querySelectorAll('button')
                );
                for (const btn of allButtons) {
                    // 检查button是否可见
                    const rect = btn.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        const btnText = btn.textContent.trim();
                        if (btnText) {  // 只添加有文本的button
                            // 生成XPath用于精确定位
                            function getXPath(element) {
                                if (element.id !== '') {
                                    return '//*[@id="' + element.id + '"]';
                                }
                                if (element === document.body) {
                                    return '/html/body';
                                }
                                let ix = 0;
                                const siblings = element.parentNode.childNodes;
                                for (let i = 0; i < siblings.length; i++) {
                                    const sibling = siblings[i];
                                    if (sibling === element) {
                                        return getXPath(element.parentNode) +
                                            '/' +
                                            element.tagName.toLowerCase() +
                                            '[' + (ix + 1) + ']';
                                    }
                                    if (sibling.nodeType === 1 &&
                                        sibling.tagName === element.tagName) {
                                        ix++;
                                    }
                                }
                            }

                            buttons.push({
                                text: btnText,
                                className: btn.className || '',
                                id: btn.id || '',
                                xpath: getXPath(btn)
                            });
                        }
                    }
                }

                console.log('在容器中找到button数量:', buttons.length);

                return {
                    parentContainerId: parentContainer.id || '',
                    parentContainerClass: parentContainer.className || '',
                    buttons: buttons
                };
            }
        """)

        if not result:
            print("        [镜像] ✗ 未找到容器priceDetail_ecs_image_table")
            return

        buttons_info = result.get('buttons', [])
        if not buttons_info:
            print("        [镜像] ✗ 未找到button")
            print(f"          父容器ID: {result.get('parentContainerId', '')}")
            parent_class = result.get('parentContainerClass', '')
            print(f"          父容器Class: {parent_class}")
            return

        print(f"        [镜像] 找到 {len(buttons_info)} 个button")
        print(f"          父容器ID: {result.get('parentContainerId', '')}")

        # 点击找到的button
        for i, btn_info in enumerate(buttons_info, 1):
            try:
                btn_text = btn_info.get('text', '')
                if not btn_text:
                    continue

                total = len(buttons_info)
                print(
                    f"        [镜像] [{i}/{total}] "
                    f"正在点击: {btn_text}"
                )

                # 优先使用XPath定位，如果不行则使用在容器内定位
                btn_element = None
                xpath = btn_info.get('xpath', '')

                if xpath:
                    try:
                        btn_element = page.locator(f'xpath={xpath}').first
                        if not btn_element.is_visible(timeout=1000):
                            btn_element = None
                    except Exception:
                        btn_element = None

                # 如果XPath定位失败，尝试在容器内定位
                if not btn_element:
                    try:
                        # 在容器内查找button
                        container = page.locator(
                            '#priceDetail_ecs_image_table'
                        )
                        btn_element = container.locator(
                            f'button:has-text("{btn_text}")'
                        ).first
                    except Exception:
                        btn_element = None

                # 如果还是失败，使用全局文本定位
                if not btn_element:
                    btn_element = page.locator(
                        f'button:has-text("{btn_text}")'
                    ).first

                # 尝试点击button
                try:
                    if btn_element.is_visible(timeout=2000):
                        btn_element.scroll_into_view_if_needed()
                        time.sleep(0.5)
                        btn_element.click(timeout=2000)
                        print(f"          ✓ 已点击: {btn_text}")
                        time.sleep(1)

                        # 点击镜像button后，提取规格价格表格
                        price_data = extract_price_tables(page)
                        if price_data:
                            images_data.append({
                                'image': btn_text,
                                'price_data': price_data
                            })
                    else:
                        # 如果不可见，尝试使用JavaScript直接点击
                        print(
                            f"        [尝试JS点击] button不可见，"
                            f"尝试使用JavaScript点击: {btn_text}"
                        )
                        clicked = page.evaluate(f"""
                            () => {{
                                const container = document.getElementById(
                                    'priceDetail_ecs_image_table'
                                );
                                if (!container) return false;
                                const buttons = Array.from(
                                    container.querySelectorAll('button')
                                );
                                for (const btn of buttons) {{
                                    const btnText = btn.textContent.trim();
                                    if (btnText === '{btn_text}') {{
                                        const rect =
                                            btn.getBoundingClientRect();
                                        if (rect.width > 0 &&
                                            rect.height > 0) {{
                                            btn.scrollIntoView(
                                                {{block: 'center'}}
                                            );
                                            btn.click();
                                            return true;
                                        }}
                                    }}
                                }}
                                return false;
                            }}
                        """)
                        if clicked:
                            print(f"          ✓ 已通过JavaScript点击: {btn_text}")
                            time.sleep(1)

                            # 点击镜像button后，提取规格价格表格
                            price_data = extract_price_tables(page)
                            if price_data:
                                images_data.append({
                                    'image': btn_text,
                                    'price_data': price_data
                                })
                        else:
                            print(f"          ✗ button不可见且JS点击失败: {btn_text}")
                except Exception as e:
                    print(f"          ✗ 点击button '{btn_text}' 时出错: {e}")
                    # 尝试使用JavaScript点击
                    try:
                        clicked = page.evaluate(f"""
                            () => {{
                                const container = document.getElementById(
                                    'priceDetail_ecs_image_table'
                                );
                                if (!container) return false;
                                const buttons = Array.from(
                                    container.querySelectorAll('button')
                                );
                                for (const btn of buttons) {{
                                    const btnText = btn.textContent.trim();
                                    if (btnText === '{btn_text}') {{
                                        btn.scrollIntoView(
                                            {{block: 'center'}}
                                        );
                                        btn.click();
                                        return true;
                                    }}
                                }}
                                return false;
                            }}
                        """)
                        if clicked:
                            print(f"          ✓ 已通过JavaScript点击: {btn_text}")
                            time.sleep(1)

                            # 点击镜像button后，提取规格价格表格
                            price_data = extract_price_tables(page)
                            if price_data:
                                images_data.append({
                                    'image': btn_text,
                                    'price_data': price_data
                                })
                    except Exception:
                        pass

            except Exception as e:
                btn_text = btn_info.get('text', '')
                print(f"          ✗ 点击button '{btn_text}' 时出错: {e}")
                continue

        print(
            f"        [镜像] ✓ 已完成所有button的点击"
            f"（共 {len(buttons_info)} 个）"
        )
        return images_data

    except Exception as e:
        print(f"        [镜像] ✗ 查找镜像button时出错: {e}")
        import traceback
        traceback.print_exc()
        return images_data


def extract_price_tables(page: Page) -> Optional[Dict]:
    """提取规格价格表格信息，返回价格数据"""
    print("\n          [规格价格] 开始提取规格价格表格...")

    # 等待页面更新，确保表格已经出现
    time.sleep(1.5)

    try:
        # 使用JavaScript提取表格信息
        result = page.evaluate("""
            () => {
                // 找到完全匹配"规格价格"的span或label元素
                let priceEl = null;

                // 先尝试查找span元素
                const spans = Array.from(
                    document.querySelectorAll('span')
                );
                for (const span of spans) {
                    const text = span.textContent.trim();
                    if (text === '规格价格') {
                        priceEl = span;
                        break;
                    }
                }

                // 如果没找到span，尝试查找label元素
                if (!priceEl) {
                    const labels = Array.from(
                        document.querySelectorAll('label')
                    );
                    for (const label of labels) {
                        const text = label.textContent.trim();
                        if (text === '规格价格') {
                            priceEl = label;
                            break;
                        }
                    }
                }

                if (!priceEl) {
                    console.log('未找到规格价格span或label');
                    return null;
                }

                // 找到该元素的父容器（包含该元素的div）
                let current = priceEl.parentElement;
                let priceDiv = null;

                // 向上查找，直到找到div容器
                while (current && current !== document.body) {
                    if (current.tagName === 'DIV') {
                        priceDiv = current;
                        break;
                    }
                    current = current.parentElement;
                }

                if (!priceDiv) {
                    console.log('未找到包含规格价格的div');
                    return null;
                }

                console.log('找到规格价格div:', priceDiv.id || priceDiv.className);

                // 找到priceDiv的父容器
                const parentContainer = priceDiv.parentElement;
                if (!parentContainer) {
                    console.log('未找到父容器');
                    return null;
                }

                // 找到父容器下的所有直接子div（按DOM顺序）
                const allDivs = Array.from(parentContainer.children).filter(
                    child => child.tagName === 'DIV'
                );

                // 找到priceDiv在allDivs中的索引
                const priceDivIndex = allDivs.indexOf(priceDiv);
                if (priceDivIndex === -1) {
                    console.log('未找到规格价格div在父容器中的索引');
                    return null;
                }

                // 找到priceDiv后面的下一个同级别div
                if (priceDivIndex + 1 >= allDivs.length) {
                    console.log('未找到后面的同级别div');
                    return {
                        containerId: priceDiv.id || '',
                        parentContainerId: parentContainer.id || '',
                        priceDivIndex: priceDivIndex,
                        totalDivs: allDivs.length,
                        dataTable: null
                    };
                }

                const tableDiv = allDivs[priceDivIndex + 1];
                console.log('找到表格div，索引:', priceDivIndex + 1);

                // 在表格div中查找所有table元素
                const tables = Array.from(
                    tableDiv.querySelectorAll('table')
                );

                if (tables.length === 0) {
                    console.log('未找到表格');
                    return {
                        containerId: priceDiv.id || '',
                        parentContainerId: parentContainer.id || '',
                        priceDivIndex: priceDivIndex,
                        totalDivs: allDivs.length,
                        dataTable: null
                    };
                }

                console.log('找到表格数量:', tables.length);

                // 查找表头表格：在tableDiv的同级别div下面查找
                let headerTable = null;
                let dataTableEl = null;
                
                // 方法1: 在tableDiv的同级别div下查找表头table
                // 表头table在详细价格table父div（tableDiv）的同级别div下面
                // 先检查tableDiv后面的同级别div
                for (let i = priceDivIndex + 2; i < allDivs.length; i++) {
                    const candidateDiv = allDivs[i];
                    const candidateTables = Array.from(
                        candidateDiv.querySelectorAll('table')
                    );
                    if (candidateTables.length > 0) {
                        headerTable = candidateTables[0];
                        console.log('在同级别div下找到表头表格，div索引:', i);
                        break;
                    }
                }
                
                // 方法2: 如果方法1没找到，检查tableDiv之前的同级别div
                if (!headerTable && priceDivIndex > 0) {
                    for (let i = priceDivIndex - 1; i >= 0; i--) {
                        const candidateDiv = allDivs[i];
                        const candidateTables = Array.from(
                            candidateDiv.querySelectorAll('table')
                        );
                        if (candidateTables.length > 0) {
                            headerTable = candidateTables[0];
                            console.log('在tableDiv之前的同级别div找到表头表格，div索引:', i);
                            break;
                        }
                    }
                }
                
                // 方法3: 如果方法1和2都没找到，在tableDiv中查找第一个table作为表头
                if (!headerTable && tables.length > 1) {
                    headerTable = tables[0];
                    console.log('在tableDiv中找到第一个table作为表头');
                }
                
                // 提取数据表格：优先使用第二个表格，如果没有则使用第一个
                const targetTableIndex = tables.length > 1 ? 1 : 0;
                if (tables.length > 0) {
                    dataTableEl = tables[targetTableIndex];
                    console.log('使用表格索引:', targetTableIndex, '作为数据表格');
                }

                // 提取表头
                let headers = [];
                if (headerTable) {
                    const headerRows = Array.from(
                        headerTable.querySelectorAll('tr')
                    );
                    const headerData = [];
                    for (const row of headerRows) {
                        const cells = Array.from(
                            row.querySelectorAll('th, td')
                        );
                        const rowData = cells.map(cell => {
                            return cell.textContent.trim();
                        });
                        if (rowData.length > 0) {
                            headerData.push(rowData);
                        }
                    }
                    
                    // 合并所有表头行（如果有多个表头行）
                    if (headerData.length > 0) {
                        if (headerData.length === 1) {
                            headers = headerData[0];
                        } else {
                            // 合并多个表头行
                            headers = headerData[0];
                            for (let i = 1; i < headerData.length; i++) {
                                headers = headers.map((h, idx) => {
                                    return idx < headerData[i].length
                                        ? (h + ' ' + headerData[i][idx]).trim()
                                        : h;
                                });
                            }
                        }
                    }
                    console.log('提取到表头:', headers);
                }

                // 提取数据行
                let dataRows = [];
                if (dataTableEl) {
                    const rows = Array.from(dataTableEl.querySelectorAll('tr'));
                    for (const row of rows) {
                        const cells = Array.from(
                            row.querySelectorAll('th, td')
                        );
                        const rowData = cells.map(cell => {
                            return cell.textContent.trim();
                        });
                        if (rowData.length > 0) {
                            dataRows.push(rowData);
                        }
                    }
                    console.log('提取到数据行数:', dataRows.length);
                }
                
                // 如果没有找到表头，尝试从数据表格的第一行提取
                if (headers.length === 0 && dataRows.length > 0) {
                    headers = dataRows[0];
                    dataRows = dataRows.slice(1);
                    console.log('从数据表格第一行提取表头');
                }
                
                const resultTable = {
                    headers: headers,
                    rowCount: dataRows.length,
                    data: dataRows
                };
                
                dataTable = resultTable;

                return {
                    containerId: priceDiv.id || '',
                    parentContainerId: parentContainer.id || '',
                    priceDivIndex: priceDivIndex,
                    totalDivs: allDivs.length,
                    dataTable: dataTable
                };
            }
        """)

        if not result:
            print("          [规格价格] ✗ 未找到规格价格span/label或容器")
            return

        print(f"          [规格价格] 找到容器: {result.get('containerId', '')}")
        print(f"          父容器ID: {result.get('parentContainerId', '')}")
        print(f"          规格价格div索引: {result.get('priceDivIndex', -1)}")
        print(f"          总div数量: {result.get('totalDivs', 0)}")

        # 显示价格表格
        data_table = result.get('dataTable')
        if data_table:
            print("\n          [规格价格] ===== 价格表格 =====")
            headers = data_table.get('headers', [])
            if headers:
                header_str = " | ".join(headers)
                print(f"          表头: {header_str}")
            print(f"          数据行数: {data_table.get('rowCount', 0)}")
            table_data = data_table.get('data', [])
            for i, row in enumerate(table_data, 1):
                row_str = " | ".join(row)
                print(f"          第{i}行: {row_str}")
        else:
            print("          [规格价格] ✗ 未找到价格表格")
            return None

        # 返回价格数据
        price_data = {
            'data_table': data_table
        }
        return price_data

    except Exception as e:
        print(f"          [规格价格] ✗ 提取表格时出错: {e}")
        import traceback
        traceback.print_exc()
        return None


def click_spec_buttons(
    page: Page, url_type: Optional[str] = None
) -> List[Dict]:
    """查找并点击规格同级别下的所有button，返回规格数据"""
    print("\n      [规格] 开始查找规格label...")
    spec_label = find_spec_label(page)

    if not spec_label:
        print("      [规格] ✗ 未找到规格label，跳过")
        return []

    # 查找规格同级别下的button
    spec_buttons = find_buttons_below_label(page, spec_label, "规格")

    if not spec_buttons:
        print("      [规格] ✗ 未找到规格同级别下的button")
        return []

    # 过滤和去重
    valid_spec_buttons = filter_valid_buttons(spec_buttons)

    if not valid_spec_buttons:
        print("      [规格] ✗ 未找到有效的规格button")
        return []

    print(f"      [规格] 找到 {len(valid_spec_buttons)} 个规格button:")
    for i, btn_info in enumerate(valid_spec_buttons, 1):
        print(f"        {i}. {btn_info['text']}")

    specs_data = []  # 存储所有规格数据

    # 点击所有规格button
    print(
        f"      [规格] 开始点击规格button"
        f"（共 {len(valid_spec_buttons)} 个）..."
    )
    for i, btn_info in enumerate(valid_spec_buttons, 1):
        try:
            btn_text = btn_info['text']
            total = len(valid_spec_buttons)
            print(f"      [规格] [{i}/{total}] 正在点击: {btn_text}")

            btn_element = btn_info['element']

            # 滚动到元素可见
            btn_element.scroll_into_view_if_needed()
            time.sleep(0.5)

            # 点击button
            if btn_element.is_visible(timeout=2000):
                btn_element.click(timeout=2000)
                print(f"        ✓ 已点击: {btn_text}")
            else:
                print(f"        ✗ button不可见: {btn_text}")
                continue

            # 等待页面响应
            time.sleep(1)

            # 如果是ECS，在点击规格button后，查找并点击同级别div下的button
            if url_type == 'ecs':
                spec_details = find_and_click_buttons_in_sibling_divs(
                    page, spec_label
                )
                if spec_details:
                    specs_data.extend(spec_details)
                else:
                    # 如果没有详细信息，至少记录规格名称
                    specs_data.append({
                        'spec': btn_text,
                        'images': []
                    })

        except Exception as e:
            print(f"        ✗ 点击button '{btn_text}' 时出错: {e}")
            continue

    print(
        f"      [规格] ✓ 已完成所有规格button的点击"
        f"（共 {len(valid_spec_buttons)} 个）"
    )
    return specs_data


def click_all_buttons(
    page: Page,
    valid_buttons: List[Dict],
    url_type: Optional[str] = None
) -> List[Dict]:
    """点击所有区域button，并在每次点击后点击可用区button、CPU架构button和规格button，返回区域数据"""
    if not valid_buttons:
        print("\n未找到任何button")
        print("建议：检查页面元素，可能需要调整选择器")
        return []

    print(f"\n找到 {len(valid_buttons)} 个区域button:")
    for i, btn_info in enumerate(valid_buttons, 1):
        print(f"  {i}. {btn_info['text']}")

    print("\n开始点击各个区域button...")
    print(f"共需要点击 {len(valid_buttons)} 个区域button\n")

    regions_data = []  # 存储所有区域数据

    for i, btn_info in enumerate(valid_buttons, 1):
        try:
            btn_text = btn_info['text']
            total = len(valid_buttons)
            print(f"[{i}/{total}] 正在点击区域button: {btn_text}")

            btn_element = btn_info['element']

            # 滚动到元素可见
            btn_element.scroll_into_view_if_needed()
            time.sleep(0.5)

            # 点击区域button
            if btn_element.is_visible(timeout=2000):
                btn_element.click(timeout=2000)
                print(f"  ✓ 已点击区域button: {btn_text}")
            else:
                print(f"  ✗ 区域button不可见: {btn_text}")
                continue

            # 等待页面响应
            time.sleep(1)

            # 点击区域button后，查找并点击可用区button
            zones_data = click_zone_buttons(page, url_type)
            if zones_data:
                regions_data.append({
                    'region': btn_text,
                    'zones': zones_data
                })
            else:
                # 如果没有可用区数据，至少记录区域名称
                regions_data.append({
                    'region': btn_text,
                    'zones': []
                })

        except Exception as e:
            print(f"  ✗ 点击区域button '{btn_text}' 时出错: {e}")
            continue

    print(f"\n✓ 已完成所有区域button的点击（共 {len(valid_buttons)} 个）")
    return regions_data


# SQLAlchemy 基础类和模型定义
Base = declarative_base()


class ECSPrice(Base):
    """ECS价格数据模型"""
    __tablename__ = 'ecs_prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(String(255), nullable=False, index=True)
    zone = Column(String(255), nullable=False, index=True)
    cpu_arch = Column(String(255), nullable=False, index=True)
    spec = Column(String(255), nullable=False, index=True)
    image = Column(String(255), nullable=False, index=True)
    price_table_data = Column(Text, nullable=False)
    created_at = Column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'region', 'zone', 'cpu_arch', 'spec', 'image',
            name='uq_ecs_price'
        ),
        Index('idx_region', 'region'),
        Index('idx_zone', 'zone'),
        Index('idx_cpu_arch', 'cpu_arch'),
        Index('idx_spec', 'spec'),
        Index('idx_image', 'image'),
    )

    def _parse_price_table(self) -> Tuple[List[str], List[List[str]]]:
        """
        解析价格表格数据，返回表头和数据行
        
        返回:
            (headers, data_rows) 元组
        """
        price_table = json.loads(self.price_table_data)
        
        # 处理新格式（包含headers和data）和旧格式（只有data数组）
        if isinstance(price_table, dict) and 'headers' in price_table:
            # 新格式：包含表头和数据
            headers = price_table.get('headers', [])
            data = price_table.get('data', [])
        elif isinstance(price_table, list) and len(price_table) > 0:
            # 旧格式：第一行作为表头，其余作为数据
            headers = price_table[0] if price_table else []
            data = price_table[1:] if len(price_table) > 1 else []
        else:
            # 空数据
            headers = []
            data = []
        
        return headers, data

    def get_headers(self) -> List[str]:
        """获取表头列表"""
        headers, _ = self._parse_price_table()
        return headers

    def get_data_rows(self) -> List[List[str]]:
        """获取数据行列表（不包括表头）"""
        _, data = self._parse_price_table()
        return data

    def get_column_data(self, column_index: int) -> List[str]:
        """
        获取指定列的所有数据（不包括表头）
        
        参数:
            column_index: 列索引（从0开始）
        
        返回:
            该列的所有数据值列表
        """
        _, data = self._parse_price_table()
        column_values = []
        for row in data:
            if column_index < len(row):
                column_values.append(row[column_index])
        return column_values

    def get_column_by_name(self, column_name: str) -> List[str]:
        """
        根据列名获取该列的所有数据
        
        参数:
            column_name: 列名（表头中的名称）
        
        返回:
            该列的所有数据值列表，如果列名不存在则返回空列表
        """
        headers, _ = self._parse_price_table()
        try:
            column_index = headers.index(column_name)
            return self.get_column_data(column_index)
        except ValueError:
            return []

    def get_all_columns(self) -> Dict[str, List[str]]:
        """
        获取所有列的数据，以列名为键
        
        返回:
            字典，键为列名，值为该列的所有数据
        """
        headers, data = self._parse_price_table()
        result = {}
        for col_idx, header in enumerate(headers):
            result[header] = []
            for row in data:
                if col_idx < len(row):
                    result[header].append(row[col_idx])
        return result

    def to_dict(self) -> Dict:
        """转换为字典，清晰区分表头和数据"""
        headers, data = self._parse_price_table()
        
        return {
            'id': self.id,
            'region': self.region,
            'zone': self.zone,
            'cpu_arch': self.cpu_arch,
            'spec': self.spec,
            'image': self.image,
            'price_table': {
                'headers': headers,  # 表头，清晰标识
                'data': data  # 数据行，不包括表头
            },
            'created_at': self.created_at
        }

    def to_dict_with_columns(self) -> Dict:
        """
        转换为字典，按列组织数据（方便按列查看）
        
        返回:
            包含按列名组织的数据的字典
        """
        headers, data = self._parse_price_table()
        
        return {
            'id': self.id,
            'region': self.region,
            'zone': self.zone,
            'cpu_arch': self.cpu_arch,
            'spec': self.spec,
            'image': self.image,
            'price_table': {
                'headers': headers,
                'data': data,
                'columns': self.get_all_columns()  # 按列名组织的数据
            },
            'created_at': self.created_at
        }


def get_engine(db_path: str):
    """
    创建数据库引擎
    
    注意：对于同步操作，使用标准 sqlite 驱动
    如果需要异步支持，可以使用 get_async_engine 函数
    """
    engine = create_engine(
        f'sqlite:///{db_path}',
        echo=False,
        pool_pre_ping=True,
        connect_args={'check_same_thread': False}
    )
    return engine


def init_database(db_path: str) -> None:
    """初始化SQLite数据库并创建表"""
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    print(f"✓ 数据库已初始化: {db_path}")


# 异步支持函数（可选，用于将来的异步操作）
async def get_async_engine(db_path: str):
    """
    创建异步数据库引擎（使用 aiosqlite）
    
    注意：这需要配合异步代码使用，当前主流程是同步的
    """
    try:
        from sqlalchemy.ext.asyncio import create_async_engine
        engine = create_async_engine(
            f'sqlite+aiosqlite:///{db_path}',
            echo=False,
            pool_pre_ping=True
        )
        return engine
    except ImportError:
        raise ImportError(
            "需要安装 sqlalchemy[asyncio] 和 aiosqlite 以支持异步操作"
        )


def write_to_sqlite(data: List[Dict], db_path: str) -> None:
    """将收集的数据写入SQLite数据库"""
    print(f"\n正在将数据写入数据库 {db_path}...")

    # 初始化数据库
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    created_at = datetime.now().isoformat()
    inserted_count = 0
    updated_count = 0
    skipped_count = 0

    try:
        for region_data in data:
            region = region_data.get('region', '未知区域')

            zones = region_data.get('zones', [])
            for zone_data in zones:
                zone = zone_data.get('zone', '未知可用区')

                cpu_archs = zone_data.get('cpu_archs', [])
                for cpu_arch_data in cpu_archs:
                    cpu_arch = cpu_arch_data.get('cpu_arch', '未知CPU架构')

                    specs = cpu_arch_data.get('specs', [])
                    for spec_data in specs:
                        spec = spec_data.get('spec', '未知规格')

                        images = spec_data.get('images', [])
                        for image_data in images:
                            image = image_data.get('image', '未知镜像')
                            price_data = image_data.get('price_data', {})

                            # 将价格表格数据转换为JSON字符串（包含表头和数据）
                            data_table = price_data.get('data_table')
                            if not data_table:
                                skipped_count += 1
                                continue

                            # 构建包含表头和数据行的完整结构
                            price_table_structure = {
                                'headers': data_table.get('headers', []),
                                'data': data_table.get('data', [])
                            }
                            price_table_json = json.dumps(
                                price_table_structure,
                                ensure_ascii=False
                            )

                            # 使用 SQLAlchemy 的 merge 或 upsert 操作
                            try:
                                # 检查是否已存在
                                existing = session.query(ECSPrice).filter(
                                    ECSPrice.region == region,
                                    ECSPrice.zone == zone,
                                    ECSPrice.cpu_arch == cpu_arch,
                                    ECSPrice.spec == spec,
                                    ECSPrice.image == image
                                ).first()

                                if existing:
                                    # 更新现有记录
                                    existing.price_table_data = (
                                        price_table_json
                                    )
                                    existing.created_at = created_at
                                    updated_count += 1
                                else:
                                    # 插入新记录
                                    new_price = ECSPrice(
                                        region=region,
                                        zone=zone,
                                        cpu_arch=cpu_arch,
                                        spec=spec,
                                        image=image,
                                        price_table_data=price_table_json,
                                        created_at=created_at
                                    )
                                    session.add(new_price)
                                    inserted_count += 1

                            except Exception as e:
                                print(f"  ✗ 插入数据时出错: {e}")
                                print(f"    区域: {region}, 可用区: {zone}, "
                                      f"CPU架构: {cpu_arch}, 规格: {spec}, "
                                      f"镜像: {image}")
                                skipped_count += 1
                                continue

        session.commit()
        print("\n✓ 数据已成功写入数据库")
        print(f"  插入: {inserted_count} 条")
        print(f"  更新: {updated_count} 条")
        print(f"  跳过: {skipped_count} 条")
        print(f"  总计: {inserted_count + updated_count} 条")

    except Exception as e:
        session.rollback()
        print(f"✗ 写入数据库时出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


def write_to_markdown(data: List[Dict], output_path: str) -> None:
    """将收集的数据写入Markdown文件"""
    print(f"\n正在将数据写入 {output_path}...")

    md_content = "# 华为云 ECS 价格信息\n\n"
    md_content += (
        "本文档包含按区域、可用区、CPU架构、规格、镜像、"
        "规格价格组织的ECS价格信息。\n\n"
    )

    for region_data in data:
        region = region_data.get('region', '未知区域')
        md_content += f"## {region}\n\n"

        zones = region_data.get('zones', [])
        for zone_data in zones:
            zone = zone_data.get('zone', '未知可用区')
            md_content += f"### {zone}\n\n"

            cpu_archs = zone_data.get('cpu_archs', [])
            for cpu_arch_data in cpu_archs:
                cpu_arch = cpu_arch_data.get('cpu_arch', '未知CPU架构')
                md_content += f"#### {cpu_arch}\n\n"

                specs = cpu_arch_data.get('specs', [])
                for spec_data in specs:
                    spec = spec_data.get('spec', '未知规格')
                    md_content += f"##### {spec}\n\n"

                    images = spec_data.get('images', [])
                    for image_data in images:
                        image = image_data.get('image', '未知镜像')
                        price_data = image_data.get('price_data', {})

                        md_content += f"**镜像**: {image}\n\n"

                        # 写入价格表格
                        data_table = price_data.get('data_table')
                        if data_table:
                            data_rows = data_table.get('data', [])
                            if data_rows:
                                md_content += "**价格详情**:\n\n"
                                # 使用第一行作为表头
                                header_line = " | ".join(data_rows[0])
                                md_content += f"| {header_line} |\n"
                                sep_line = " | ".join(
                                    ["---"] * len(data_rows[0])
                                )
                                md_content += f"| {sep_line} |\n"
                                # 从第二行开始写入数据
                                for row in data_rows[1:]:
                                    row_line = " | ".join(row)
                                    md_content += f"| {row_line} |\n"
                                md_content += "\n"

                        md_content += "---\n\n"

    # 确保输出目录存在
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"✓ 数据已成功写入 {output_path}")


def process_url(
    url: str,
    labels: Optional[List[str]] = None,
    url_type: Optional[str] = None
) -> List[Dict]:
    """处理单个URL，返回收集的数据"""
    if labels is None:
        labels = []
    with sync_playwright() as p:
        browser, page = setup_browser(p)
        try:
            # 1. 进入页面
            navigate_to_page(page, url)

            # 2. 关闭弹窗
            close_popups(page)

            # 3. 进入价格详情
            price_detail_clicked = click_price_detail(page)
            if price_detail_clicked:
                # 等待价格详情页面加载
                print("等待价格详情页面加载...")
                time.sleep(2)

            # 4. 查找区域label
            region_element = find_region_label(page)

            # 5. 查找区域下面的button
            buttons = find_buttons_below_region(page, region_element)

            # 6. 过滤和去重button
            valid_buttons = filter_valid_buttons(buttons)

            # 7. 点击所有区域button，并在每次点击后点击可用区button
            regions_data = click_all_buttons(page, valid_buttons, url_type)

            # 如果没有找到button，保存截图
            if not valid_buttons:
                page.screenshot(path="page_screenshot.png")
                print("已保存截图到 page_screenshot.png")

            return regions_data

        finally:
            # 保持浏览器打开一段时间以便查看
            print("\n等待5秒后关闭浏览器...")
            time.sleep(5)
            browser.close()


def query_ecs_prices(
    db_path: str,
    region: Optional[str] = None,
    zone: Optional[str] = None,
    cpu_arch: Optional[str] = None,
    spec: Optional[str] = None,
    image: Optional[str] = None,
    limit: int = 100,
    with_columns: bool = False
) -> List[Dict]:
    """
    查询ECS价格数据

    参数:
        db_path: 数据库路径
        region: 区域（可选）
        zone: 可用区（可选）
        cpu_arch: CPU架构（可选）
        spec: 规格（可选）
        image: 镜像（可选）
        limit: 返回结果数量限制
        with_columns: 是否按列组织数据（默认False，返回标准格式）

    返回:
        价格数据列表，每个元素包含：
        - id, region, zone, cpu_arch, spec, image, created_at
        - price_table: {
            'headers': [表头列表],  # 清晰标识表头
            'data': [数据行列表],   # 数据行，不包括表头
            'columns': {...}        # 仅当with_columns=True时包含，按列名组织
          }
    """
    engine = get_engine(db_path)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # 构建查询
        query = session.query(ECSPrice)

        # 添加过滤条件
        if region:
            query = query.filter(ECSPrice.region == region)
        if zone:
            query = query.filter(ECSPrice.zone == zone)
        if cpu_arch:
            query = query.filter(ECSPrice.cpu_arch == cpu_arch)
        if spec:
            query = query.filter(ECSPrice.spec == spec)
        if image:
            query = query.filter(ECSPrice.image == image)

        # 限制结果数量
        results = query.limit(limit).all()

        # 转换为字典列表
        if with_columns:
            return [price.to_dict_with_columns() for price in results]
        else:
            return [price.to_dict() for price in results]

    finally:
        session.close()


def query_ecs_prices_by_column(
    db_path: str,
    column_name: str,
    region: Optional[str] = None,
    zone: Optional[str] = None,
    cpu_arch: Optional[str] = None,
    spec: Optional[str] = None,
    image: Optional[str] = None,
    limit: int = 100
) -> Dict:
    """
    按列查询ECS价格数据，返回指定列的所有值
    
    参数:
        db_path: 数据库路径
        column_name: 要查询的列名（表头中的名称）
        region: 区域（可选）
        zone: 可用区（可选）
        cpu_arch: CPU架构（可选）
        spec: 规格（可选）
        image: 镜像（可选）
        limit: 返回结果数量限制
    
    返回:
        字典，包含：
        - 'column_name': 列名
        - 'headers': 所有表头（用于参考）
        - 'metadata': 每条记录的元数据列表
        - 'column_values': 该列的所有值列表
        - 'total_records': 记录总数
        - 'total_values': 值总数
    """
    engine = get_engine(db_path)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # 构建查询
        query = session.query(ECSPrice)

        # 添加过滤条件
        if region:
            query = query.filter(ECSPrice.region == region)
        if zone:
            query = query.filter(ECSPrice.zone == zone)
        if cpu_arch:
            query = query.filter(ECSPrice.cpu_arch == cpu_arch)
        if spec:
            query = query.filter(ECSPrice.spec == spec)
        if image:
            query = query.filter(ECSPrice.image == image)

        # 限制结果数量
        results = query.limit(limit).all()

        # 提取指定列的数据
        metadata_list = []
        column_values = []
        all_headers = set()

        for price in results:
            # 获取表头
            headers = price.get_headers()
            all_headers.update(headers)

            # 获取元数据
            metadata_list.append({
                'id': price.id,
                'region': price.region,
                'zone': price.zone,
                'cpu_arch': price.cpu_arch,
                'spec': price.spec,
                'image': price.image,
                'created_at': price.created_at
            })

            # 获取指定列的数据
            values = price.get_column_by_name(column_name)
            column_values.extend(values)

        return {
            'column_name': column_name,
            'headers': list(all_headers),  # 所有可能的表头
            'metadata': metadata_list,
            'column_values': column_values,
            'total_records': len(metadata_list),
            'total_values': len(column_values)
        }

    finally:
        session.close()


def query_all_columns(
    db_path: str,
    region: Optional[str] = None,
    zone: Optional[str] = None,
    cpu_arch: Optional[str] = None,
    spec: Optional[str] = None,
    image: Optional[str] = None,
    limit: int = 100
) -> Dict[str, Dict]:
    """
    查询所有列的数据，按列名组织（方便一列一列查看）
    
    参数:
        db_path: 数据库路径
        region: 区域（可选）
        zone: 可用区（可选）
        cpu_arch: CPU架构（可选）
        spec: 规格（可选）
        image: 镜像（可选）
        limit: 返回结果数量限制
    
    返回:
        字典，键为记录ID，值为：
        {
            'metadata': {
                'region': ...,
                'zone': ...,
                ...
            },
            'headers': [表头列表],  # 清晰标识表头
            'columns': {列名: [值列表]}  # 按列名组织的数据
        }
    """
    engine = get_engine(db_path)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # 构建查询
        query = session.query(ECSPrice)

        # 添加过滤条件
        if region:
            query = query.filter(ECSPrice.region == region)
        if zone:
            query = query.filter(ECSPrice.zone == zone)
        if cpu_arch:
            query = query.filter(ECSPrice.cpu_arch == cpu_arch)
        if spec:
            query = query.filter(ECSPrice.spec == spec)
        if image:
            query = query.filter(ECSPrice.image == image)

        # 限制结果数量
        results = query.limit(limit).all()

        # 按记录组织所有列的数据
        result_dict = {}
        for price in results:
            result_dict[price.id] = {
                'metadata': {
                    'region': price.region,
                    'zone': price.zone,
                    'cpu_arch': price.cpu_arch,
                    'spec': price.spec,
                    'image': price.image,
                    'created_at': price.created_at
                },
                'headers': price.get_headers(),  # 清晰标识表头
                'columns': price.get_all_columns()  # 按列名组织的数据
            }

        return result_dict

    finally:
        session.close()


def main():
    """主函数"""
    for key, config in huawei_urls.items():
        url = config['url']
        labels = config.get('labels', [])
        regions_data = process_url(url, labels, key)

        # 将数据写入SQLite数据库
        if regions_data:
            db_path = (
                Path(__file__).parent.parent.parent / 'src' /
                'huawei_cloud_ops_mcp_server' / 'huaweicloud' /
                'pricedocs' / 'price.db'
            )
            # 确保目录存在
            db_path.parent.mkdir(parents=True, exist_ok=True)
            write_to_sqlite(regions_data, str(db_path))
            print(f"\n数据库路径: {db_path}")
            print("\n查询示例:")
            print("\n  # 1. 基本查询（表头和数据清晰区分）")
            print("  from script.price.get_ecs_price import query_ecs_prices")
            print("  results = query_ecs_prices("
                  "str(db_path), region='华北-北京四')")
            print("  for r in results:")
            print("      print('表头:', r['price_table']['headers'])")
            print("      print('数据:', r['price_table']['data'])")
            print("\n  # 2. 按列查询（方便一列一列查看数据）")
            print("  from script.price.get_ecs_price import "
                  "query_ecs_prices_by_column")
            print("  column_data = query_ecs_prices_by_column("
                  "str(db_path), column_name='价格', "
                  "region='华北-北京四')")
            print("  print('列名:', column_data['column_name'])")
            print("  print('该列的所有值:', column_data['column_values'])")
            print("\n  # 3. 查询所有列（按列名组织）")
            print("  from script.price.get_ecs_price import "
                  "query_all_columns")
            print("  all_columns = query_all_columns("
                  "str(db_path), region='华北-北京四')")
            print("  for record_id, data in all_columns.items():")
            print("      print('表头:', data['headers'])")
            print("      print('按列组织的数据:', data['columns'])")
            print("\n  # 4. 查询时包含按列组织的数据")
            print("  results = query_ecs_prices("
                  "str(db_path), region='华北-北京四', "
                  "with_columns=True)")
            print("  # 结果中包含 'columns' 字段，按列名组织")
        else:
            print("\n未收集到任何数据，跳过写入数据库")


if __name__ == "__main__":
    main()
